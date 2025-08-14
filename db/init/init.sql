-- =====================
-- Création des tables
-- =====================

-- Table roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    permission VARCHAR(100) NOT NULL
);

-- Table status
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    status VARCHAR(50) NOT NULL
);

-- Table clients
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    role_id INT NOT NULL REFERENCES roles(id),
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    adresse TEXT NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Table articles
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prix NUMERIC(10,2) NOT NULL,
    categorie VARCHAR(50) NOT NULL,
    description TEXT,
    stock INT NOT NULL
);

-- Table commandes
CREATE TABLE commandes (
    id SERIAL PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients(id),
    status_id INT NOT NULL REFERENCES status(id),
    prix NUMERIC(10,2) NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Table commandes_articles (relation n-n)
CREATE TABLE commandes_articles (
    id SERIAL PRIMARY KEY,
    commande_id INT NOT NULL REFERENCES commandes(id),
    article_id INT NOT NULL REFERENCES articles(id),
    quantite INT NOT NULL
);

-- =====================
-- Insertion de données
-- =====================

-- Roles
INSERT INTO roles (nom, permission) VALUES
('admin', 'all'),
('client', 'read,write');

-- Status
INSERT INTO status (status) VALUES
('en attente'),
('en cours'),
('terminée');

-- Clients
INSERT INTO clients (role_id, nom, prenom, adresse, telephone, email, username, password) VALUES
(2, 'Dupont', 'Jean', '1 rue A, Paris', '0601020304', 'jean.dupont@example.com', 'jdupont', 'motdepasse'),
(2, 'Martin', 'Alice', '12 avenue B, Lyon', '0605060708', 'alice.martin@example.com', 'amartin', 'motdepasse');

-- Articles
INSERT INTO articles (nom, prix, categorie, description, stock) VALUES
('Tacos', 49.99, 'Plat', 'meilleur tacos', 10),
('Pizza thon', 149.99, 'Plat', 'Best pizza', 5),
('Chocolat', 129.99, 'Dessert', 'En or', 20);

-- Commandes
INSERT INTO commandes (client_id, status_id, prix, date) VALUES
(1, 1, 199.97, NOW()),
(2, 2, 49.99, NOW());

-- Commandes_Articles
INSERT INTO commandes_articles (commande_id, article_id, quantite) VALUES
(1, 1, 2),  -- 2 Tacos
(1, 2, 1),  -- 1 pizza thon
(2, 1, 1);  -- 1 Tacos pour la commande 2
