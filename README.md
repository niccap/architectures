# Software Architectures for Enterprise Systems

This repository contains source code, examples, and exercises for the **Software Architectures for Enterprise Systems** course.

The material supports the lab sessions and illustrates web service development, communication between components, data persistence, containerization, and the deployment of distributed systems. It also includes the Adventure Builder architecture documentation as a case study.

## Repository structure

| Directory | Contents |
| --- | --- |
| [`adventure-builder/`](adventure-builder/) | Static architecture documentation for the Adventure Builder case study, including diagrams and reusable view and interface templates. |
| [`docker/`](docker/) | Introductory examples of Dockerfiles, Docker Compose, and Compose Watch. |
| [`kubernetes/`](kubernetes/) | Sample manifests for applications and MongoDB, including Deployments, Services, ConfigMaps, Secrets, and dashboard configuration. |
| [`lab1/`](lab1/) | Jupyter notebooks and examples of HTTP API usage with Python, including requests to weather forecast services. |
| [`lab2/`](lab2/) | Introduction to REST services with Flask and Waitress: Hello World, country management, and a car inventory. |
| [`lab3/`](lab3/) | Containerization of REST services with Docker. |
| [`lab4/`](lab4/) | Client-server applications, graphical clients with Kivy/KivyMD, and authentication exercises. |
| [`lab5/`](lab5/) | Data persistence with SQLite and MySQL, initialization scripts, and Docker Compose configurations. |
| [`lab6/`](lab6/) | Service composition for car inventory management and VIN decoding, UML diagrams, and deployment examples with Docker Compose and Kubernetes. |
| [`lab7/`](lab7/) | Asynchronous communication with RabbitMQ: producers and consumers, work queues, publish/subscribe, and routing. |

## Adventure Builder architecture documentation

**[Browse the Adventure Builder documentation](https://niccap.github.io/architectures/)** on GitHub Pages.

Adventure Builder is an educational adventure travel e-commerce application. Its Software Architecture Document covers module, runtime, and allocation views, service interfaces, requirements, and mappings between views. The site includes architecture diagrams, downloadable Visio files, and reusable architecture view and interface templates.

The original documentation was written by **Paulo Merson and Darpan Saini**, Software Engineering Institute / Carnegie Mellon University, and accompanies *Documenting Software Architectures: Views and Beyond, Second Edition* (2010). This edition reorganizes the historical material and preserves its existing TODOs and open decisions.

You can also open [`adventure-builder/index.html`](adventure-builder/index.html) locally without a server or an Internet connection. See the [Adventure Builder README](adventure-builder/README.md) for editing, generation, validation, and publishing instructions. The GitHub Pages workflow publishes only the documentation site's generated pages and assets.

## Technologies used

- **Python** and **Jupyter Notebook** for examples and exercises.
- **Flask**, **Waitress**, and **Requests** for exposing and consuming HTTP APIs.
- **Kivy** and **KivyMD** for graphical clients.
- **SQLite**, **MySQL**, and **PyMySQL** for data persistence.
- **RabbitMQ** and **Pika** for messaging.
- **Docker**, **Docker Compose**, and **Kubernetes** for containerization and orchestration.
- **PlantUML** for class and sequence diagrams.
- **HTML**, **CSS**, and **JavaScript** for the static Adventure Builder documentation, with **Python** scripts for generation and validation.

## Running a first example

To run the country REST service from lab 2, create a virtual environment and install the required dependencies from the repository root.

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install flask waitress
python lab2/countries.py
```

On Windows, activate the virtual environment in PowerShell with `.\.venv\Scripts\Activate.ps1`, then run the same installation and startup commands.

The service is available at `http://localhost:8080`. From another terminal, query the list of countries:

```bash
curl http://localhost:8080/countries
```

Stop the service with `Ctrl+C`.

## Working with the labs

The examples are independent and may require additional dependencies or services. Before running an example, consult its source code, exercise comments, and any Dockerfiles, Compose files, or Kubernetes manifests in the relevant directory.

Notebooks require a Jupyter environment; the MySQL and RabbitMQ examples require their respective servers. Containerization examples require Docker and Docker Compose, while Kubernetes examples require a cluster and a configured `kubectl` client.

Many HTTP services use port `8080`: run them one at a time or adjust their ports. When an example accesses local files using relative paths, run it from its own directory.

The code and configurations are intended for educational use and provide a starting point for studying and completing the course exercises.
