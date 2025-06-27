from setuptools import setup, find_packages

setup(
    name='DocumentAnalyzer',
    version='0.1.0',
    author='Ananya Mehta',
    author_email='amehta@parkar.digital',
    description='An AI-powered Policy Assistant',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'streamlit',
        'sentence-transformers',
        'optimum[onnxruntime]',
        'onnxruntime',
        'transformers',
        'faiss-cpu',
        'pytesseract',
        'Pillow',
        'PyPDF2',
        'python-docx',
        'langdetect'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            # Uncomment and adjust the following line if you want a CLI entry point
            # 'document-analyzer=src.app:main',
        ],
    },
)
