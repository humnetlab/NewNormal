# UCI calculation run script
# Execution: load config -> process each metro/season -> output

library(yaml)
library(purrr)
library(readr)
library(progress)

source('uci_utils.R')

cfg <- yaml::read_yaml('data/fig3/metros.yml')$metros
codes <- vapply(cfg, `[[`, "code", FUN.VALUE = character(1))
cfg_lookup <<- setNames(cfg, codes)  # global assignment for utils functions

out <- list(
  cache = 'cache/tigris',
  trips = 'trips',
  csv   = 'results/csv'
)
dir.create(out$csv, recursive = TRUE, showWarnings = FALSE)

cbd_meta <- read_cbd_meta('data/fig3/cbd_lat-lon.csv')

uci_idx <- tibble::tibble(metro = character(), season = character(), index = numeric())
uci_met <- tibble::tibble()

total_runs <- sum(purrr::map_int(cfg, function(m) {
  length(list.dirs(file.path(out$trips, m$code), recursive = FALSE, full.names = FALSE))
}))
pb <- progress_bar$new(
  format = '  Now :metro/:season [:bar] :percent ETA :eta',
  total  = total_runs, clear = FALSE
)

# main
for (m in cfg) {
  metro_code <- m$code
  all_seasons <- list.dirs(file.path(out$trips, metro_code),
                           recursive = FALSE, full.names = FALSE)
  base_seasons <- unique(gsub("-2$", "", all_seasons))

  for (base_season in base_seasons) {
    season_variants <- all_seasons[grepl(paste0("^", base_season, "(-2)?$"), all_seasons)]

    pb$tick(tokens = list(metro = metro_code, season = base_season))

    res <- proc_metro_season(
      metro    = metro_code,
      season   = base_season,
      season_dirs = season_variants,
      cfg      = list(
        state    = m$states,
        year     = 2020,
        counties = m$counties,
        exclude  = character(0)
      ),
      out      = out,
      cbd_meta = cbd_meta
    )

    uci_idx <- dplyr::bind_rows(uci_idx,
                         tibble::tibble(metro = metro_code, season = base_season, index = res$index))
    uci_met <- dplyr::bind_rows(uci_met, res$metrics)
  }
}

readr::write_csv(uci_idx, file.path(out$csv, 'uci_index.csv'))
readr::write_csv(uci_met, file.path(out$csv, 'uci_metrics.csv'))

message('done!')
