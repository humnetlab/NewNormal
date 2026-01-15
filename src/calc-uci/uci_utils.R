library(sf)
library(dplyr)
library(stringr)
library(classInt)
library(glue)
library(readr)
library(uci)
library(tigris)
options(tigris_use_cache = TRUE)
library(yaml)
library(purrr)

read_cbd_meta <- function(path = 'data/fig3/cbd_lat-long.csv') {
  read_csv(path, col_types = cols(
    name  = col_character(),
    lat   = col_double(),
    long  = col_double(),
    metro = col_character()
  ))
}

# geometry cache (once)
# county cbgs -> 50km buffer -> largest connected component

read_cbgs <- function(metro, cache = 'cache/tigris') {
  shp_dir  <- file.path(cache, metro, 'cbg')
  shp_file <- file.path(shp_dir, 'cbgs.shp')

  if (!file.exists(shp_file)) {
    message("cbgs.shp not found for ", metro, " refetching")
    cfg         <- cfg_lookup[[metro]]
    exclude_vec <- if (!is.null(cfg$exclude)) cfg$exclude else character(0)
    year_val    <- if (!is.null(cfg$year)) cfg$year else 2020

    full <- get_cbgs(
      state_abbr = cfg$states,
      year       = year_val,
      counties5  = cfg$counties,
      exclude    = exclude_vec,
      cache      = cache,
      metro      = metro
    )

    dir.create(shp_dir, recursive = TRUE, showWarnings = FALSE)
    st_write(full,
             dsn           = shp_dir,
             layer         = 'cbgs',
             driver        = 'ESRI Shapefile',
             delete_layer  = TRUE,
             quiet         = TRUE)
  }

  st_read(shp_file, quiet = TRUE) %>% mutate(GEOID = as.character(GEOID))
}

read_cbg_buffer <- function(metro, cache = 'cache/tigris',
                            mode = c("within", "intersect"),
                            force_rebuild = FALSE) {
  mode <- match.arg(mode)

  shp_dir  <- file.path(cache, metro, 'cbg_buffer')
  shp_file <- file.path(shp_dir, 'cbgs_buffer.shp')

  mode_file   <- file.path(shp_dir, 'cbgs_buffer_mode.txt')
  cached_mode <- if (file.exists(mode_file)) readLines(mode_file, warn = FALSE) else NA_character_

  if (force_rebuild || !file.exists(shp_file) || is.na(cached_mode) || cached_mode != mode) {
    message("Building 50km buffer with mode = '", mode, "' for ", metro)
    full   <- read_cbgs(metro, cache)
    cbd_pt <- cbd_meta %>% dplyr::filter(metro == !!metro) %>% dplyr::slice(1)
    buffer <- filter_cbgs_by_buffer(full, cbd_pt, radius_km = 50, mode = mode)

    dir.create(shp_dir, recursive = TRUE, showWarnings = FALSE)
    st_write(buffer,
             dsn           = shp_dir,
             layer         = 'cbgs_buffer',
             driver        = 'ESRI Shapefile',
             delete_layer  = TRUE,
             quiet         = TRUE)
    writeLines(mode, con = mode_file)
  }

  st_read(shp_file, quiet = TRUE) %>% dplyr::mutate(GEOID = as.character(GEOID))
}

read_cbg_connected <- function(metro, cache = 'cache/tigris') {
  shp_dir  <- file.path(cache, metro, 'cbg_connected')
  shp_file <- file.path(shp_dir, 'cbgs_connected.shp')

  if (!file.exists(shp_file)) {
    message("cbgs_connected.shp not found", metro, " extracting largest connected component")
    buffer    <- read_cbg_buffer(metro, cache)
    connected <- extract_largest_component(buffer)

    dir.create(shp_dir, recursive = TRUE, showWarnings = FALSE)
    st_write(connected,
             dsn           = shp_dir,
             layer         = 'cbgs_connected',
             driver        = 'ESRI Shapefile',
             delete_layer  = TRUE,
             quiet         = TRUE)

    n_components <- length(unique(get_connected_components(buffer)))
    message(sprintf("  Metro: %s | Buffer CBGs: %d | Components: %d | Largest: %d (%.1f%%)",
                    metro, nrow(buffer), n_components, nrow(connected),
                    100 * nrow(connected) / nrow(buffer)))
  }

  st_read(shp_file, quiet = TRUE) %>% mutate(GEOID = as.character(GEOID))
}

get_connected_components <- function(sf_data) {
  adj_matrix <- st_touches(sf_data, sparse = FALSE)
  n <- nrow(sf_data)
  components <- integer(n)
  current_component <- 1L
  for (i in seq_len(n)) {
    if (components[i] == 0L) {
      stack <- i
      while (length(stack) > 0L) {
        current <- stack[[length(stack)]]
        stack <- stack[-length(stack)]
        if (components[current] == 0L) {
          components[current] <- current_component
          neighbors <- which(adj_matrix[current, ])
          unvisited <- neighbors[components[neighbors] == 0L]
          if (length(unvisited)) stack <- c(stack, unvisited)
        }
      }
      current_component <- current_component + 1L
    }
  }
  components
}

extract_largest_component <- function(sf_data) {
  components <- get_connected_components(sf_data)
  component_sizes <- tabulate(components, nbins = max(components))
  largest_component_id <- which.max(component_sizes)
  sf_data[components == largest_component_id, ]
}

get_cbgs <- function(state_abbr, year = 2020, counties5, exclude,
                     cache = 'cache/tigris', metro) {
  stopifnot(!missing(metro))
  subdir   <- file.path(cache, metro, 'cbg')
  dir.create(subdir, recursive = TRUE, showWarnings = FALSE)
  shp_file <- file.path(subdir, 'cbgs.shp')
  if (file.exists(shp_file)) {
    return(st_read(shp_file, quiet = TRUE) %>% mutate(GEOID = as.character(GEOID)))
  }
  counties_by_state <- split(counties5, substr(counties5, 1, 2))
  cbgs_list <- purrr::imap(counties_by_state, function(c5, st_fips) {
    tigris::block_groups(
      state  = st_fips,
      county = unique(substr(c5, 3, 5)),
      year   = year,
      cb     = TRUE
    )
  })
  cbgs <- dplyr::bind_rows(cbgs_list) %>%
    dplyr::mutate(GEOID = as.character(GEOID)) %>%
    dplyr::filter(substr(GEOID,1,5) %in% counties5, !GEOID %in% exclude)

  st_write(cbgs, dsn = subdir, layer = 'cbgs',
           driver = 'ESRI Shapefile', delete_layer = TRUE, quiet = TRUE)
  cbgs
}

filter_cbgs_by_buffer <- function(cbgs, cbd_point, radius_km = 50,
                                  mode = c('within', 'intersect')) {
  mode <- match.arg(mode)
  cbd_sf     <- st_sfc(st_point(c(cbd_point$long, cbd_point$lat)), crs = 4326)
  target_crs <- st_crs(cbgs)
  cbd_buff   <- st_transform(cbd_sf, target_crs) %>% st_buffer(radius_km * 1000)
  cbgs_tran  <- st_transform(cbgs, target_crs) %>% sf::st_make_valid()
  idx <- if (mode == 'intersect') {
    lengths(st_intersects(cbgs_tran, cbd_buff)) > 0
  } else {
    lengths(st_covered_by(cbgs_tran, cbd_buff)) > 0
  }
  cbgs_tran[idx, ]
}

read_cbg_grid <- function(metro, season, base = 'trips') {
  dir <- file.path(base, metro, season, 'cbg')
  shp <- list.files(dir, pattern = 'destination_layer.*\\.shp$', full.names = TRUE)[1]
  if (is.na(shp)) stop('no data in ', dir)
  st_read(shp, quiet = TRUE) %>%
    dplyr::mutate(
      GEOID  = stringr::str_pad(as.character(customGeo), 12, 'left', '0'),
      destin = as.numeric(destin),
      sqmi   = as.numeric(sqmi),
      sqkm   = sqmi * 2.58999
    )
}

# main: load geometries, join trips, calculate UCI
proc_metro_season <- function(metro, season, season_dirs, cfg, out, cbd_meta) {
  cbgs_full <- read_cbgs(metro, cache = out$cache)
  cbgs_filt <- read_cbg_connected(metro, cache = out$cache)

  grd_all <- purrr::map_dfr(season_dirs, function(sea) {
    read_cbg_grid(metro, sea, base = out$trips)
  })

  df <- cbgs_filt %>%
    dplyr::left_join(
      grd_all %>%
        sf::st_drop_geometry() %>%
        dplyr::group_by(GEOID) %>%
        dplyr::summarize(
          destin = sum(destin, na.rm = TRUE),
          sqkm   = dplyr::first(sqkm),
          .groups = "drop"
        ),
      by = 'GEOID'
    ) %>%
    dplyr::mutate(
      destin     = dplyr::coalesce(destin, 0),
      sqkm       = dplyr::coalesce(sqkm, as.numeric(ALAND) / 1e6),
      data_avail = GEOID %in% grd_all$GEOID
    )

  miss <- is.na(df$centrLon) | is.na(df$centrLat) | df$centrLon == 0 | df$centrLat == 0
  if (any(miss)) {
    cent <- sf::st_centroid(df[miss, ]) %>% sf::st_coordinates()
    df$centrLon[miss] <- cent[,1]; df$centrLat[miss] <- cent[,2]
  }

  dist_type <- if (metro %in% c('bos','sf','ny')) 'spatial_link' else 'euclidean'
  u <- uci(sf_object = df, var_name = 'destin', dist_type = dist_type,
           bootstrap_border = FALSE, showProgress = FALSE)

  message(sprintf("  %s/%s: Full CBGs=%d | Connected=%d | Data avail=%d | Filled=%d | UCI=%.6f",
                  metro, season, nrow(cbgs_full), nrow(df),
                  sum(df$data_avail), sum(!df$data_avail), u$UCI[1]))

  list(index = u$UCI[1],
       metrics = u %>% tibble::as_tibble() %>% dplyr::mutate(metro = metro, season = season))
}
