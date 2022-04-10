import os

DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://faozuispekgops"
                                              ":49e44fdedf916d54c5d562385a7677a6f387af7111403befac06fa0b2f96c73b@ec2"
                                              "-176-34-116-203.eu-west-1.compute.amazonaws.com:5432/d1gec1g9j9v7sr")

SECRET_KEY: str = os.getenv("SECRET_KEY", "abobik")
ALGORITHMS_JWT: str = os.getenv("ALGORITHMS_JWT", "HS256")