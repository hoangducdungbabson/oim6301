# TV Show Catalog ERD

```mermaid
erDiagram
    TV_SHOW ||--o{ SHOW_CREDIT : has
    PERSON ||--o{ SHOW_CREDIT : receives
    TV_SHOW ||--o{ SHOW_GENRE : has
    GENRE ||--o{ SHOW_GENRE : classifies
    TV_SHOW ||--o| SHOW_RATING : has

    TV_SHOW {
        int show_id PK
        string title
        int release_year
        string show_type
        int episode_count
    }

    PERSON {
        int person_id PK
        string full_name
        int birth_year
    }

    SHOW_CREDIT {
        int show_id PK, FK
        int person_id PK, FK
        string credit_role PK
    }

    GENRE {
        int genre_id PK
        string genre_name
    }

    SHOW_GENRE {
        int show_id PK, FK
        int genre_id PK, FK
    }

    SHOW_RATING {
        int show_id PK, FK
        decimal average_rating
        int vote_count
    }
```

## Assumptions

- Different shows can share a title, and different people can share a name. Each show and person has a separate ID.
- A person can be both a star and a writer on the same show. Each show, person, and role combination appears at most once.
- A show can be listed before any credits or genres are recorded. A genre can be listed before any show uses it.
- Each show has at most one current rating summary. A show without a rating has no row in `SHOW_RATING`.