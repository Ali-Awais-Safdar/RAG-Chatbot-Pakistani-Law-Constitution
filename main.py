import pytest

if __name__ == "__main__":
    pytest.main(["-k", "TestTokenizeLegalText or TestCleanLegalText or TestNormalizeLegalText"]) # added the class names to run specific tests
