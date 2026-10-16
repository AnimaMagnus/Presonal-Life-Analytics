create schema if not exists life;
set search_path to life;

-- 1. Users
create table users(
    user_id uuid primary key default gen_random_uuid(),
    email text not null unique,
    display_name text,
    timezone text not null default 'UTC',
    base_currency char(3) not null default 'EUR',
    created_at timestamptz not null default now()
);

-- Automatically refresh updated_at when a row is changed
create function set_updated_at()
returns trigger AS $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

-- 2. Daily check-ins (log)
create table daily_checkins(
    checkin_id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(user_id) on delete cascade,
    checkin_date date not null,
    sleep_hours numeric(3, 1) check (sleep_hours between 0 and 24),
    mood smallint check (mood between 1 and 5),
    energy smallint check (energy between 1 and 5),
    productivity smallint check (productivity between 1 and 5),
    gratitude text,
    went_well text,
    was_hard text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (user_id, checkin_date)
);

create trigger trg_daily_checkins_updated
    before update on daily_checkins
    for each row execute function set_updated_at();

-- 3. Habits (definition)
create table habits(
    habit_id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(user_id) on delete cascade,
    name text not null,
    target_count smallint not null default 1 check (target_count > 0),
    target_period text not null default 'day' check (target_period in ('day', 'week', 'month')),
    is_active boolean not null default true,
    created_at timestamptz not null default now()
);
create index idx_habits_user on habits (user_id);

-- 4. Habit checks (log)
create table habit_checks(
    habit_check_id uuid primary key default gen_random_uuid(),
    habit_id uuid not null references habits(habit_id) on delete cascade,
    check_date date not null,
    done boolean not null,
    unique (habit_id, check_date)
);

-- 5. Tasks (one-off to-dos)
create table tasks(
    task_id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(user_id) on delete cascade,
    title text not null,
    planned_date date not null,
    done boolean not null default false,
    completed_at timestamptz,
    created_at timestamptz not null default now(),
    check ((done and completed_at is not null)
        or (not done and completed_at is null))
);
create index idx_tasks_user_date on tasks (user_id, planned_date);

-- 6. Categories (definition)
create table categories(
    category_id uuid primary key default gen_random_uuid(),
    user_id uuid references users(user_id) on delete cascade,
    name text not null,
    kind text not null check (kind in ('expense', 'income'))
);
create unique index uq_categories_owner_kind_name
on categories(
             coalesce(user_id, '00000000-0000-0000-0000-000000000000'::uuid),
             kind,
             lower(name)
    );

-- 7. Transactions (log)
create table transactions(
    transaction_id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(user_id) on delete cascade,
    occurred_at timestamptz not null,
    amount numeric(12,2) not null check (amount > 0),
    currency char(3) not null,
    type text not null check (type in ('expense', 'income', 'savings')),
    category_id uuid references categories(category_id),
    note text,
    created_at timestamptz not null default now()
);
create index idx_transactions_user_time on transactions (user_id, occurred_at);

-- 8. Goals (definition)
create table goals(
    goal_id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(user_id) on delete cascade,
    name text not null,
    section text not null check (section in ('personal', 'finance')),
    target_value numeric not null check (target_value > 0),
    unit text not null,
    start_date date not null default current_date,
    deadline date,
    status text not null default 'active' check (status in ('active', 'achieved', 'dropped')),
    created_at timestamptz not null default now(),
    check (deadline is null or deadline >= start_date)
);
create index idx_goals_user on goals (user_id);

-- 9. Goal update (log)
create table goal_updates(
    update_id uuid primary key default gen_random_uuid(),
    goal_id uuid not null references goals(goal_id) on delete cascade ,
    update_date date not null,
    current_value numeric not null check (current_value >= 0),
    note text,
    unique (goal_id, update_date)
);

-- 10. Seed data
insert into categories (user_id, name, kind) values
    (NULL, 'Food', 'expense'),
    (NULL, 'Transport', 'expense'),
    (NULL, 'Housing', 'expense'),
    (NULL, 'Leisure', 'expense'),
    (NULL, 'Health', 'expense'),
    (NULL, 'Subscriptions', 'expense'),
    (NULL, 'Education', 'expense'),
    (NULL, 'Other', 'expense'),
    (NULL, 'Salary', 'income'),
    (NULL, 'Side income', 'income'),
    (NULL, 'Other', 'income');

select * from categories;

select current_database();