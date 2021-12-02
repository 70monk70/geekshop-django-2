from locust import HttpUser, TaskSet, task


def login(l):
    data = {
        "username": "apl",
        "password": "1"
    }
    l.client.post("/users/login/", data)


def logout(l):
    data = {
        "username": "apl",
        "password": "1"
    }
    l.client.post("/users/logout/", data)

# def orders(l):
#     l.client.get("/orders/")


def index(l):
    l.client.get("/")

# def profile(l):
#     l.client.get("auth/edit/")


def products(l):
    l.client.get("/products/")


@task
class UserBehavior(TaskSet):
    tasks = {index: 5, products: 5}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)

@task
class WebsiteUser(HttpUser):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
