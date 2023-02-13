**Условия голосоввания:**
1) Нельзя голосовать за себя 
2) Нельзя голосовать за своего руководителя
3) Голосовать можно только за одного человека


**Steps to Build & Push Docker image to GitLab repository**

1) Login: ```docker login registry.gitlab.com```

2) Build: ```docker build -t registry.gitlab.com/shinhan-finance/hr-rating-system . --platform linux/amd64```

3) Push: ```docker push registry.gitlab.com/shinhan-finance/hr-rating-system```
