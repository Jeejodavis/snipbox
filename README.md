# snipbox

Snipbox is a django restframework project with JWT authentication, user management and snippet management. Create snippet with tag and manage.

Requirements are added in the requirement.txt file

Features
- JWT authentication (`SimpleJWT`)
- Login (`authentication` app)
- Snippet management (`snippets` app)  
  - Create / list / update / delete snippets  
  - Snippet -> Tag relationship  
  - Only show logged-in user’s snippets  
  - Snippet list includes `detail` link
  - Delete API returns the snippet list
- Tag management  
  - List all tags  
  - View tag detail with all snippets under that tag
- PostgreSQL database with `.env` configuration
- Clean project structure (`snipbox/`, `config/`)

