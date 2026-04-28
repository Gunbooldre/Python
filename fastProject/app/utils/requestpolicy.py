from typing import Protocol, Callable
from functools import reduce
from urllib.request import Request


# Class example


class RequestPolicy(Protocol):
    def apply(self, request) -> None: ...


class ActivePolicy:
    def apply(self, request) -> None:
        if not request.is_active:
            raise Exception("Request is not active")


class MfaRequiredPolicy:
    def apply(self, request) -> None:
        if not request.is_mfa_required:
            raise Exception("MFA is required")


class RoleRequiredPolicy:
    def apply(self, request) -> None:
        if request.role != "admin":
            raise Exception("Role is required")


class CompositePolicy:
    def __init__(self, policies: list[RequestPolicy]) -> None:
        self.policies = policies

    def apply(self, request) -> None:
        for policy in self.policies:
            policy.apply(request)


policy = CompositePolicy([ActivePolicy(), MfaRequiredPolicy(), RoleRequiredPolicy()])  # etc

# Fuction example

type Policyfn = Callable[[Request], Request]
request = "www.google.com"  # example


def active_user(request:Request):
    if not request.is_active:
        raise Exception("Request is not active")
    return request


def role_required(request:Request):
    if request.role != "admin":
        raise Exception("Role is required")
    return request


def mfa_required(request:Request):
    if not request.is_mfa_required:
        raise Exception("MFA is required")
    return request


def apply_policies(request:Request, policies: list[Policyfn]) -> Request:
    return reduce(lambda current, policy: policy(current), policies, request)


policies = [active_user, role_required, mfa_required]  # etc
request = apply_policies(request, policies)
