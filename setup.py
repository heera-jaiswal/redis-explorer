from setuptools import setup, find_packages
setup(
    name='redis_explorer',
    version='1.0',
    description='Redis Explorer',
    author='Heera Jaiswal',
    include_package_data = True,
#    package_data={"": ["*.ini"]},
    install_requires=[
                    "requests==2.12.3"                    
                    ,"Flask"
                    ,"flask-restful"
                    ,"redis"
                    ,"flask-swagger==0.2.13"
                    ,"memory-profiler"                         
                    ,"uwsgi"
    			],
    #setup_requires=["virtualenv"],
    packages = find_packages()
    )