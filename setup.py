from setuptools import setup, find_packages

setup(
    name="tetris_game",
    version="0.2.0",
    description="俄罗斯方块游戏",
    author="Tetris Game Team",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ]
    },
    python_requires=">=3.7",
)
