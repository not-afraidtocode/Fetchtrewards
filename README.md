# Endpoint Availability Monitor - Fetch SRE Exercise  
Hi! This is my submission for Fetch's Site Reliability Engineering take-home exercise. The tool monitors HTTP endpoints, checks their availability every 15 seconds, and reports statistics based on response time and status codes.  

## Table of Contents  
- [Installation](#installation)  
- [Usage](#usage)  
- [Sample Configuration](#sample-configuration)  
- [Testing](#testing)  

---

## Installation  

Follow these steps to set up the project:  

1. **Clone the repository**:  
   
   ```
   bash  
   git clone https://github.com/<your-username>/fetch-sre-exercise.git  
   cd fetch-sre-exercise  
   ```

2. **Install dependencies**

   ```
   bash  
   pip3 install -r requirements.txt  
   ```
## Usage

Run the `reliable.py` with a YAML configuration file:
   
   ```
   bash 
   python3 monitor.py path/to/config.yaml  
   ```
   **example: python3 monitor.py sample_config.yaml**  
   
   **Output:**
```
   jsonplaceholder.typicode.com: 100.00% availability  
   example.com: 0.00% availability  
   self-signed.badssl.com: 0.00% availability  
 ``` 

## Sample Configuration

The included sample_config.yaml demonstrates:

| Endpoint Name          | URL                                          | Purpose                               |
| --- | --- | --- |
| Healthy POST Endpoint  | https://jsonplaceholder.typicode.com/posts   | Valid POST request with headers/body  |
| Simple GET Endpoint    | https://jsonplaceholder.typicode.com/todos/1 | Valid GET request (no optional fields)|
| Port Handling Test     | http://example.com:8080/health               | Domain grouping ignores port numbers  |
| SSL Failure Test       | https://self-signed.badssl.com               | Invalid SSL certificate handling      |

## Testing

**Unit testing**

``` 
python3 -m unittest test_monitor.py -v
``` 
----
