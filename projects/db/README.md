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
        string work_email UK
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