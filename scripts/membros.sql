insert into auth_user(password, last_login, is_superuser, username, first_name,
                      last_name, email, is_staff, is_active, date_joined)
VALUES
    ('golf1995',null, false, 'kercianogueira', 'Kercia', 'Nogueira', 'kercia@email.com', false, true, '2022-11-08 02:52:03.667324 +00:00'),
    ('golf1995',null, false, 'igordinizf', 'Igor', 'Ramon', 'igor@email.com', false, true, '2022-11-08 02:52:03.667324 +00:00'),
    ('golf1995',null, false, 'emersondesaa', 'Emerson', 'De Sa', 'emersondesaa@email.com', false, true, '2022-11-08 02:52:03.667324 +00:00'),
    ('golf1995',null, false, 'kamillysamp', 'Kamy', 'Saulo', 'kamy@email.com', false, true, '2022-11-08 02:52:03.667324 +00:00'),
    ('golf1995',null, false, 'bruna.f.martins', 'Bruna', 'Fernandes', 'bruna@email.com', false, true, '2022-11-08 02:52:03.667324 +00:00'),
    ('golf1995',null, false, 'antoniomarquesprimeiro', 'Antonio', 'Marques', 'marques@email.com', false, true, '2022-11-08 02:52:03.667324 +00:00'),
    ('golf1995',null, false, 'henriquealmeidaa', 'Henrique', 'Almeida', 'henrique@email.com', false, true, '2022-11-08 02:52:03.667324 +00:00'),
    ('golf1995',null, false, 'jvqueirozzz', 'Joao', 'Victor', 'joao@email.com', false, true, '2022-11-08 02:52:03.667324 +00:00');


INSERT INTO gerenciamento_membro(nome, email, data_entrada, foto, status, nota, user_id)
VALUES
    ('Kercia', 'kercia@email.com', '2021-07-07 12:00:03.667324 +00:00', 'foto', 'true', '', 2),
    ('Igor', 'igor@email.com', '2020-03-26 12:00:03.667324 +00:00', 'foto', 'true', '', 3),
    ('emersondesaa', 'emersondesaa@email.com', '2022-11-08 02:52:03.667324 +00:00', 'foto', 'true', '', 4),
    ('kamillysamp', 'kamillysamp_@email.com', '2022-11-08 02:52:03.667324 +00:00', 'foto', 'true', '', 5),
    ('bruna.f.martins', 'bruna.f.martins@email.com', '2022-11-08 02:52:03.667324 +00:00', 'foto', 'true', '', 6),
    ('antoniomarquesprimeiro', 'antoniomarquesprimeiro@email.com', '2022-11-08 02:52:03.667324 +00:00', 'foto', 'true', '', 7),
    ('henriquealmeidaa', 'henriquealmeidaa@email.com', '2022-11-08 02:52:03.667324 +00:00', 'foto', 'true', '', 8),
    ('jvqueiroz', 'jvqueirozzz@email.com', '2022-11-08 02:52:03.667324 +00:00', 'foto', 'true', '', 9);