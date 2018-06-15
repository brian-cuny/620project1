library(tidyverse)
library(ggrepel)

calc <- read_csv('C:\\Users\\Brian\\Desktop\\GradClasses\\Summer18\\620\\620project1\\calculations.csv')

airports.sub <- read_delim('C:\\Users\\Brian\\Desktop\\GradClasses\\Summer18\\620\\620project1\\openflights_airports.txt', delim=' ')


locations <- inner_join(calc, airports.sub, by=c('ID' = 'Airport ID')) %>%
  select(ID, Airport, Country.x, Centrality, Latitude, Longitude) %>%
  rename(Country = Country.x)

plotting.data <- locations %>%
  filter(Centrality > 10)

ggplot(locations) + 
  borders('world', regions = c('Canada', 'UK'), color='gray50', fill='gray50') + 
  geom_point(aes(x=Longitude, y=Latitude, color=Centrality), 
             shape=ifelse(locations$Centrality > 10, 1, 0)
  ) +
  geom_label_repel(data=plotting.data, aes(x=Longitude, y=Latitude, label=Airport)) +
  labs(x='Longitude', 
       y='Latitude',
       color='Centrality',
       title='Airports with Highest Centrality'
  )