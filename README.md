# django-simple-microservices 10web task
***
10Web company gave a task. The task would be implemented by microservices by Flask engine.
## Task Description

Imagine a platform which provides news feed service. The task is to design an architecture that
should include at least two services: a Client Service, Subscription Service and support the
following functionality.
1. Client Service: This service should handle client-related operations such as sign up,
login, and profile management. It should have its own database to store client
information. (implement only client's sign up)
2. Subscription Service: This service should manage all subscription-related operations. It
should offer multiple subscription plans, with pricing based on the client's region and
device type (e.g., USA, iOS). It should also include a subscribe functionality
implemented as an API route. The subscription plan should be chosen automatically on
clients signup based on the client's region and device type. This service should have its
own database to store subscription plan information and client subscriptions. (Implement
only choosing right subscription part, use 3 predefined plans)
3. Transaction Logic: The architecture should ensure that every client is associated with a
subscription plan and vice versa. In other words, there should not exist a client without a
subscription or a subscription without a client.
4. Front End is not required.
***

# Microservices design
High level design you can see below
![](/home/artyom/work/personal/flask-simple-microservices/flask_microservice_example-High level.drawio.png)
