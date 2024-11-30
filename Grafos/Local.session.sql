select 
    origin_city
    ,destiny_city
    ,travel_date
    ,min(price * 0.80) as price
    ,count(companies) as companies
from 
    flightsearcher.summary_view
WHERE
    org in ('GRU','BCN','LIS','MAD','CDG')
    and dest in ('GRU','BCN','LIS','MAD','CDG')
group by
    1,2,3