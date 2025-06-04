# 🐍 FastAPI PostgreSQL Posts API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

A robust FastAPI API with PostgreSQL integration, featuring authentication, CRUD operations, and comprehensive testing.

## Features

- **User Authentication**: JWT token-based authentication
- **Post Management**: Full CRUD operations for blog posts
- **Voting System**: Users can vote on posts
- **Database Integration**: SQLAlchemy with PostgreSQL
- **Automated Testing**: Comprehensive test suite with pytest
- **Docker Support**: Containerized deployment
- **CI/CD**: GitHub Actions workflow for deployment

## API Endpoints

### Authentication
- `POST /login` - User login (JWT token)
- `POST /users` - Create new user

### Posts
- `GET /posts` - Get all posts
- `GET /posts/{id}` - Get single post
- `POST /posts` - Create new post (authenticated)
- `PUT /posts/{id}` - Update post (authenticated)
- `DELETE /posts/{id}` - Delete post (authenticated)

### Votes
- `POST /vote` - Vote on a post (authenticated)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Noka993/fast-api.git
cd fast-api
```

2. Set up environment variables (create `.env` file):
```bash
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=yourpassword
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY=yoursecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
uvicorn app.main_sqlalchemy:app --reload
```
### Docker Deployment
```bash
docker-compose up -d
```
## Testing
Run the test suite with:
```bash
pytest
```
## Technologies used:
- Python 3.8+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (for migrations)
- Pytest (for testing)
- Docker (for containerization)

## License 
This project is licensed under the [MIT License](LICENSE).
