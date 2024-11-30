from  fastapi import FastAPI
import uvicorn
from api.routes.routes import routes as student_routes

app = FastAPI(
    title="Student Management API",
    description="An API for managing student records",
    version="1.0.0"
)
app.include_router(student_routes,prefix="/api")

if __name__ == '__main__':
    
    uvicorn.run(app)



