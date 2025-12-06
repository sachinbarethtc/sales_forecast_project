# # import os
# # # from pydantic import BaseSettings
# # from pydantic_settings import BaseSettings

# # class Settings(BaseSettings):
# #     db_host: str
# #     db_port: int = 5432
# #     db_name: str
# #     db_user: str
# #     db_password: str
# #     source_schema: str = "mbazaar_sandbox"
# #     source_table1: str = "generic_sales_history"
# #     source_table2: str = "generic_final_assortment"
# #     result_table: str = "forecast_results"
# #     timezone: str = "Asia/Kolkata"

# #     class Config:
# #         env_file = ".env"

# # settings = Settings()


# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     DB_HOST: str
#     DB_PORT: int = 5432
#     DB_NAME: str
#     DB_USER: str
#     DB_PASSWORD: str

#     TARGET_SCHEMA: str
#     SOURCE_TABLE1: str
#     SOURCE_TABLE2: str
#     RESULT_TABLE: str
#     TIMEZONE: str

#     class Config:
#         env_file = ".env"

# settings = Settings()


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    TARGET_SCHEMA: str
    SOURCE_TABLE1: str
    SOURCE_TABLE2: str
    RESULT_TABLE: str
    TIMEZONE: str

    class Config:
        env_file = ".env"

settings = Settings()

