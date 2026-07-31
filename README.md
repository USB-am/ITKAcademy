# Тестовое задания для ITKAcademy

  

## Stack

*  **Language:** Python 3.12

*  **Framework:** FastAPI

*  **Data base:** PostgreSQL

*  **ORM:** SQLAlchemy

*  **Migrations:** Alembic

*  **Containerization:** Docker / Docker Compose

  
  

## Quick start

Run the application via Docker Compose `sudo docker compose up -d --build`

  

Run application tests `sudo docker compose exec web pytest -v`

  

To run the application locally, you can use `run_server.sh`

  
  

## Hosts and ports

URL for manual testing

`http://localhost:8000/docs`

  

PostgreSQL uses port `5432`

  
  

## Endpoints

-  `/api/v1/wallets/{wallet_id}` get wallet balance by wallet_id

-  `/api/v1/wallets/{wallet_id}/operation` send request (DEPOSIT/WITHDRAW) to update Wallet.balance

-  `/api/v1/wallets/add` add new Wallet to database
