from fastapi import FastAPI
app = FastAPI(title="MDB-API Microservice")

# include the routes defined in api.py (/api/v1/getByName and /health)
from app.routes import router
app.include_router(router)

# run uvicorn 
if __name__ == "__main__":
    import uvicorn
    from app.env import HOST, PORT
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
