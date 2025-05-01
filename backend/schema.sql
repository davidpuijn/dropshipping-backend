create table reports (
  id uuid primary key default gen_random_uuid(),
  url text,
  status text,
  reported_at timestamp with time zone default now()
);