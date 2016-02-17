drop table if exists beer_entries;
create table beer_entries (
  id integer primary key autoincrement,
  beer_batch_number integer not null,
  beer_number_in_batch integer not null,
  beer_type text not null,
  beer_id text not null
);
