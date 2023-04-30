CREATE TABLE employers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    description TEXT)

CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    description TEXT,
    remote_work TEXT,
    salary INTEGER)

SELECT e.name, COUNT(v.id) AS vacancies_count
FROM employers e
JOIN vacancies v ON e.id = v.employer_id
GROUP BY e.name
ORDER BY vacancies_count DESC

SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.url AS vacancy_url
FROM employers e
JOIN vacancies v ON e.id = v.employer_id
ORDER BY company_name, vacancy_name

SELECT AVG((salary_from + salary_to) / 2) AS avg_salary
FROM vacancies
WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL AND salary_currency = 'RUR'

SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.url AS vacancy_url
FROM employers e
JOIN vacancies v ON e.id = v.employer_id
WHERE (salary_from + salary_to) / 2 > (
    SELECT AVG((salary_from + salary_to) / 2) AS avg_salary
    FROM vacancies
    WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL AND salary_currency = 'RUR'
)
AND salary_currency = 'RUR'
ORDER BY company_name, vacancy_name

SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.salary_currency, v.url AS vacancy_url
FROM employers e
JOIN vacancies v ON e.id = v.employer_id
WHERE LOWER(v.name) LIKE %s
ORDER BY company_name, vacancy_name