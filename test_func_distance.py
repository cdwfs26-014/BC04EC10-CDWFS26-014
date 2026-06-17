"""Tests fonctionnels d'interaction utilisateur via Selenium (navigateur reel).

Cible : l'application servie (par defaut via le grid Selenium du compose).
  - en local : RUN_SELENIUM_LOCAL=1 + chemins driver/navigateur ;
  - via le grid : docker compose -f grid/compose.yaml up -d --build,
    puis le webdriver distant se connecte au hub (http://localhost:4444).
"""

import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


@pytest.fixture()
def driver():
    load_dotenv()
    run_selenium_local = bool(os.getenv("RUN_SELENIUM_LOCAL", False))
    if run_selenium_local:
        service = webdriver.ChromeService(executable_path=os.getenv("CHROMEDRIVER_PATH"))
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.binary_location = os.getenv("CHROMEBIN_PATH")
        drv = webdriver.Chrome(service=service, options=options)
    else:
        drv = webdriver.Remote(
            command_executor="http://localhost:4444",
            options=webdriver.FirefoxOptions(),
        )
        drv.implicitly_wait(5)
    yield drv
    drv.quit()


@pytest.fixture
def target_scheme():
    load_dotenv()
    return os.getenv("TARGET_SCHEME", "http")


@pytest.fixture()
def target_host():
    load_dotenv()
    return os.getenv("TARGET_HOST", "my_distance")


@pytest.fixture()
def target_port():
    load_dotenv()
    return os.getenv("TARGET_PORT", "5000")


def test_calcul_distance_via_navigateur(driver, target_scheme, target_host, target_port):
    driver.get(f"{target_scheme}://{target_host}:{target_port}")
    # Saisie des deux points dans le formulaire
    driver.find_element(by=By.ID, value="apoint").send_keys("2,5")
    driver.find_element(by=By.ID, value="bpoint").send_keys("1,6")
    # Soumission
    driver.find_element(by=By.XPATH, value="//input[@type='submit']").click()
    # Le resultat doit etre affiche (et different de la page vide "None")
    body = driver.find_element(by=By.XPATH, value="/html/body")
    assert "result_distance" in body.text


def test_element_inexistant(driver, target_scheme, target_host, target_port):
    driver.get(f"{target_scheme}://{target_host}:{target_port}")
    with pytest.raises(NoSuchElementException):
        driver.find_element(by=By.ID, value="none")


def test_element_inexistant_liste_vide(driver, target_scheme, target_host, target_port):
    driver.get(f"{target_scheme}://{target_host}:{target_port}")
    assert len(driver.find_elements(by=By.ID, value="none")) == 0
