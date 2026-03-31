create table if not exists audit_events (
    id integer primary key autoincrement,
    identity text not null,
    endpoint text not null,
    score real not null,
    verdict text not null,
    breakdown_json text not null,
    created_at text default current_timestamp
);
