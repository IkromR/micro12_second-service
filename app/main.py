from fastapi import FastAPI, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel


class CreateLoyaltyModel(BaseModel):
    name: str


class Loyalty:
    def __init__(self, id: int, nameloyalty: str):
        self.id = id
        self.name = nameloyalty


LoyaltyList: list[Loyalty] = [
    # Loyalty(0, "30% Скидка на бытовую технику"),
    # Loyalty(1, "%15 Скидка на электронику"),
    # Loyalty(2, "Скидка %10 на продуктовые товары")

]


def add_products(content: CreateLoyaltyModel):
    id = len(LoyaltyList)
    LoyaltyList.append(Loyalty(id, content.name))
    return id


app = FastAPI()

##########
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: "loyalty-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)


#
##########

##########
# Prometheus

from prometheus_fastapi_instrumentator import Instrumentator


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#
##########


@app.get("/v1/loyalty")
async def get_loyalty():
    return LoyaltyList


@app.post("/v1/loyalty")
async def add_loyalty(content: CreateLoyaltyModel):
    add_products(content)
    return LoyaltyList[-1]


@app.get("/v1/loyalty/{id}")
async def get_loyalty_by_id(id: int):
    result = [item for item in LoyaltyList if item.id == id]
    if len(result) > 0:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@app.get("/__health")
async def check_loyalty():
    return
