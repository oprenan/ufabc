create table flightsearcher.flight (
	org text
	,dest text
	,travel_date date
	,price float
	,companies text
	,departure text
	,arrival text
	,stops int
	,layovers text
	,duration text
);

alter table flightsearcher.flight add column created_date timestamp;