# Database Project — BabsonAI Labs

## 1. The Scenario

I chose Scenario A: BabsonAI Labs.

## 2. The ERD
```mermaid
erDiagram
    PEOPLE o|--o{ PEOPLE : manages
    PEOPLE ||--o{ PROJECT_MEMBERS : participates
    PROJECTS ||--|{ PROJECT_MEMBERS : includes
    PROJECTS ||--o{ TASKS : contains
    PEOPLE o|--o{ TASKS : receives
    PROJECTS ||--o{ EXPENSES : incurs

    PEOPLE {
        int person_id PK
        string first_name
        string last_name
        string work_email 
        string title
        date start_date
        int manager_id FK
    }

    PROJECTS {
        int project_id PK
        string project_name
        string client_name
        string category
        decimal budget
        date start_date
        string status
    }

    PROJECT_MEMBERS {
        int person_id PK, FK
        int project_id PK, FK
        string project_role
        int hours_per_week
        date joined_date
    }

    TASKS {
        int task_id PK
        int project_id FK
        string description
        date created_date
        int assignee_id FK
        date assigned_date
        date due_date
        date completed_date
    }

    EXPENSES {
        int expense_id PK
        int project_id FK
        date expense_date
        decimal amount
        string category
        string note
    }
```
## 3. What One Row Means

- One row of people represents one employee at BabsonAI Labs.
- One row of projects represents one project managed by BabsonAI Labs.
- One row of project_members represents one employee's participation in one specific project, including their role, weekly hours, and joining date.
- One row of tasks represents one task belonging to one project, which may be assigned to one employee or remain unassigned.
- One row of expenses represents one individual expense incurred by one project.

## 4. Design Choices

### Keys and project membership

I use person_id as the primary key because names can be duplicated
and work emails can change. An ID keeps the employee's relationships
with other tables stable.

The project_members table uses a composite primary key consisting
of person_id and project_id. This allows an employee to participate
in multiple projects while preventing duplicate membership records
for the same employee and project. Project roles and weekly hours
belong in this table because they can differ across projects.

### Optional fields and relationships

Some fields allow NULL because the information does not always
apply. Founders may have no manager, and internal projects may have
no external client. A task may remain unassigned, so assignee_id and
assigned_date can both be NULL. A NULL completed_date means the task
has not been completed.

A project can exist without expenses. The project_spending view
keeps these projects in the results and displays their spending
as zero.

### Rules enforced by the database

Primary keys prevent duplicate identifiers, and foreign keys require
referenced records to exist. CHECK constraints require positive
budgets and expense amounts, restrict weekly membership hours to
1–40, and limit category and status values to the permitted options.

Task constraints also prevent completion before creation and require
assignee_id and assigned_date to be either both present or both NULL.
The negative-expense test demonstrates that DuckDB rejects an
expense amount of -50.00.

### Rules checked with queries

The foreign key on tasks.assignee_id ensures that the employee
exists, but it does not ensure that the employee belongs to the
task's project. A separate query compares task assignments with
project_members to identify violations. Tasks 299 and 300
intentionally violate this rule.

Other rules also require separate checks, including whether an
assignment occurs before the employee's start date and whether
every project has at least one member. The current database
constraints do not automatically enforce these rules.

### AI assistance

AI helped propose the schema, generate example code, and explain
errors during implementation.

One AI-assisted design decision was using LEFT JOIN and COALESCE
in the project_spending view. An INNER JOIN would exclude projects
without expenses, making the budget report incomplete. LEFT JOIN
keeps those projects, while COALESCE displays their total expenses
as zero instead of NULL.

I checked this behavior by viewing projects 11 and 12 in the
notebook. Both appeared with total expenses of 0.00. Their remaining
budgets were 7,000.00 and 15,000.00, matching their original budgets.
This check confirmed that the view includes projects that have not
started spending.

The first AI-generated membership check compared only the number of
violations with the expected count of two. That could pass even if two
wrong tasks were flagged. The revised check also compares the exact
ordered task IDs with [299, 300] and fails if they differ. Additional
queries check that assignments do not precede employee start dates
and that no project is missing all its members.
