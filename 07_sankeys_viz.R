library(tidyverse) 
#library(tidygraph)

library(ggalluvial)
library(gridExtra)

library(RColorBrewer)

### 

rev(brewer.pal(8, 'Blues'))[1:6]

rev(brewer.pal(6, 'Set1'))[1:6]

#### Countries

intra_country <- read_csv('05_intra_country_geography_above_20.csv')

# by decreasing

intra_flow <- ggplot(data = intra_country,
                      aes(axis1 = `Acquiror name`, axis2 = `Target name`,
                          y = `Count`)) +
  stat_alluvium(aes(fill = `Acquiror region`), 
                decreasing = FALSE) +
  geom_stratum(decreasing = FALSE) +
  geom_text(stat = "stratum", aes(label = after_stat(stratum)),
            decreasing = FALSE) +
  scale_x_discrete(limits = c("Acquiror", "Target"), expand = c(.2, .05)) +
  xlab("Intra") +
  scale_fill_manual(
    values=brewer.pal(6, 'Set1'),
    breaks=c("Asia",
             "North America",
             "Europe & Central Asia",
             "Latin America & Caribbean",
             "Caribbean",
             "Africa and Middle East"
             ),
    na.value = NA
  ) +
  #scale_color_grey(aesthetics = "fill") +
  #scale_fill_manual(values = c('#ffffcc', '#c7e9b4', '#7fcdbb', '#41b6c4', '#2c7fb8','#253494')) +
  #scale_colour_brewer(palette = "Greens")
  theme_minimal() +
  theme(legend.position = "none",
        axis.text.x = element_text(size=20),
        axis.title.x = element_text(size=30),
        axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        plot.margin = unit(c(0, 1, 0, 1), "cm")
  )

intra_flow

inward_country <- read_csv('05_inward_country_geography_above_20.csv')
# by decreasing

inward_flow <- ggplot(data = inward_country,
                aes(axis1 = `Acquiror name`, axis2 = `Target name`,
                    y = `Count`)) +
         stat_alluvium(aes(fill = `Acquiror region`), 
                       decreasing = FALSE) +
         geom_stratum(decreasing = FALSE) +
         geom_text(stat = "stratum", aes(label = after_stat(stratum)),
                   decreasing = FALSE) +
         scale_x_discrete(limits = c("Acquiror", "Target"), expand = c(.2, .05)) +
         xlab("Inward") +
  scale_fill_manual(
    values=brewer.pal(8, 'Set1'),
    breaks=c("Asia",
             "North America",
             "Europe & Central Asia",
             "Latin America & Caribbean",
             "Caribbean",
             "Africa and Middle East",
             "Sub-Saharan Africa",
             NA
    ),
    na.value = NA
  ) +
         #scale_color_grey(aesthetics = "fill") +
         #scale_fill_manual(values = c('#ffffcc', '#c7e9b4', '#7fcdbb', '#41b6c4', '#2c7fb8','#253494', 'red', 'red')) +
         theme_minimal() +
         theme(legend.position = "none",
         axis.text.x = element_text(size=20),
         axis.title.x = element_text(size=30),
         axis.text.y = element_blank(),
         axis.ticks = element_blank(),
         axis.title.y = element_blank(),
         panel.grid.major.x = element_blank(),
         panel.grid.minor.x = element_blank(),
         panel.grid.major.y = element_blank(),
         panel.grid.minor.y = element_blank(),
         plot.margin = unit(c(0, 1, 0, 1), "cm")
         )

inward_flow

outward_country <- read_csv('05_outward_country_geography_above_20.csv')

outward_flow <- ggplot(data = outward_country,
                      aes(axis1 = `Acquiror name`, axis2 = `Target name`,
                          y = `Count`)) +
  stat_alluvium(aes(fill = `Acquiror region`), 
                decreasing = FALSE) +
  geom_stratum(decreasing = FALSE) +
  geom_text(stat = "stratum", aes(label = after_stat(stratum)),
            decreasing = FALSE) +
  scale_x_discrete(limits = c("Acquiror", "Target"), expand = c(.2, .05)) +
  xlab("Outward") +
  scale_fill_manual(
    values=brewer.pal(7, 'Set1'),
    breaks=c("Asia",
             "North America",
             "Europe & Central Asia",
             "Latin America & Caribbean",
             "Caribbean",
             "Africa and Middle East",
             "Sub-Saharan Africa"
             )
    ) +
  #scale_color_grey(aesthetics = "fill") +
  #scale_fill_manual(values = c('#ffffcc', '#c7e9b4', '#7fcdbb', '#41b6c4', '#2c7fb8','#253494')) +
  theme_minimal() +
  theme(legend.position = "none",
        axis.text.x = element_text(size=20),
        axis.title.x = element_text(size=30),
        axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        plot.margin = unit(c(0, 1, 0, 1), "cm")
  )


outward_flow

pdf("Country Flows 20.pdf", width = 18, height = 12) # Open a new pdf file
grid.arrange(intra_flow, inward_flow, outward_flow,
             ncol=3,
             top=grid::textGrob('Country Flows', gp=grid::gpar(fontsize=35)))
dev.off()

########################################################

### City level

intra_city <- read_csv('06_intra_cities_over_10.csv')

# by decreasing

intra_flow <- ggplot(data = intra_city,
                     aes(axis1 = `Acquiror Standardised City`, axis2 = `Target Standardised City`,
                         y = `Count`)) +
  stat_alluvium(aes(fill = `Acquiror region`), 
                decreasing = FALSE) +
  geom_stratum(decreasing = FALSE) +
  geom_text(stat = "stratum", aes(label = after_stat(stratum)),
            decreasing = FALSE) +
  scale_x_discrete(limits = c("Acquiror", "Target"), expand = c(.2, .05)) +
  xlab("Intra") +
  scale_fill_manual(
    values=brewer.pal(7, 'Set1'),
    breaks=c("East Asia & Pacific",
             "North America",
             "Europe & Central Asia",
             "Latin America & Caribbean",
             "Caribbean",
             "Africa and Middle East",
             "Sub-Saharan Africa"
    )
  ) +
  #scale_color_grey(aesthetics = "fill") +
  #scale_fill_manual(values = c('#ffffcc', '#c7e9b4', '#7fcdbb', '#41b6c4', '#2c7fb8','#253494')) +
  theme_minimal() +
  theme(legend.position = "none",
        axis.text.x = element_text(size=20),
        axis.title.x = element_text(size=30),
        axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        plot.margin = unit(c(0, 1, 0, 1), "cm")
  )

intra_flow

inward_city <- read_csv('06_inward_cities_over_10.csv')

# by decreasing

inward_flow <- ggplot(data = inward_city,
                     aes(axis1 = `Acquiror Standardised City`, axis2 = `Target Standardised City`,
                         y = `Count`)) +
  stat_alluvium(aes(fill = `Acquiror region`), 
                decreasing = FALSE) +
  geom_stratum(decreasing = FALSE) +
  geom_text(stat = "stratum", aes(label = after_stat(stratum)),
            decreasing = FALSE) +
  scale_x_discrete(limits = c("Acquiror", "Target"), expand = c(.2, .05)) +
  xlab("Inward") +
  scale_fill_manual(
    values=brewer.pal(7, 'Set1'),
    breaks=c("East Asia & Pacific",
             "North America",
             "Europe & Central Asia",
             "Latin America & Caribbean",
             "Caribbean",
             "Africa and Middle East",
             "Sub-Saharan Africa"
    )
  ) +
  #scale_color_grey(aesthetics = "fill") +
  #scale_fill_manual(values = c('#ffffcc', '#c7e9b4', '#7fcdbb', '#41b6c4', '#2c7fb8','#253494')) +
  theme_minimal() +
  theme(legend.position = "none",
        axis.text.x = element_text(size=20),
        axis.title.x = element_text(size=30),
        axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        plot.margin = unit(c(0, 1, 0, 1), "cm")
  )

inward_flow

outward_city <- read_csv('06_outward_cities_over_10.csv')

# by decreasing

outward_flow <- ggplot(data = outward_city,
                     aes(axis1 = `Acquiror Standardised City`, axis2 = `Target Standardised City`,
                         y = `Count`)) +
  stat_alluvium(aes(fill = `Acquiror region`), 
                decreasing = FALSE) +
  geom_stratum(decreasing = FALSE) +
  geom_text(stat = "stratum", aes(label = after_stat(stratum)),
            decreasing = FALSE) +
  #geom_text(stat = "stratum",
  #          aes(label = paste0(stratum,
  #                             ifelse(nchar(as.character(stratum)) == 1L,
  #                                    ": ", "\n"),
  #                             after_stat(n))),
  #          decreasing = FALSE) +
  scale_x_discrete(limits = c("Acquiror", "Target"), expand = c(.2, .05)) +
  xlab("Outward") +
  #scale_color_grey(aesthetics = "fill") +
  scale_fill_manual(
    values=brewer.pal(7, 'Set1'),
    breaks=c("East Asia & Pacific",
             "North America",
             "Europe & Central Asia",
             "Latin America & Caribbean",
             "Caribbean",
             "Africa and Middle East",
             "Sub-Saharan Africa"
    )
  ) +
  theme_minimal() +
  theme(legend.position = "none",
        axis.text.x = element_text(size=20),
        axis.title.x = element_text(size=30),
        axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        axis.title.y = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        plot.margin = unit(c(0, 1, 0, 1), "cm")
  )

outward_flow

pdf("City Flows.pdf", width = 18, height = 12) # Open a new pdf file
grid.arrange(intra_flow, inward_flow, outward_flow,
             ncol=3,
             top=grid::textGrob('City Flows', gp=grid::gpar(fontsize=35)))
dev.off()

