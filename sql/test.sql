CREATE TABLE `users`(
  `id` INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
  `first_name` VARCHAR(30) NOT NULL,
  `last_name` VARCHAR(30) NOT NULL,
  `adress` VARCHAR(50) NOT NULL
 );
 INSERT INTO `users`(`first_name`,`last_name`,`adress`)
  VALUES('Yuka', 'Misutani', 'Kanagawa');
INSERT INTO `users`(`first_name`,`last_name`,`adress`) VALUES
 ('Ran', 'Misutani', 'Kanagawa'),
('Junko', 'Misutani', 'Kanagawa');

CREATE TABLE `goods`(
  `id` int(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  `price` int(11) NOT NULL
);

INSERT INTO `goods`(`name`,`price`) VALUES
('SQLbook', 3000),
('Python', 5000),
('HTML', 2000);

CREATE TABLE `history`(
  `id` INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
  `user_id` int(11) NOT NULL,
  `goods_id` INT(11) NOT NULL,
  `date` DATE NOT NULL,
  CONSTRAINT FOREIGN KEY `user_fk`(`user_id`) REFERENCES `users`(`id`),
  CONSTRAINT FOREIGN KEY `goods_fk`(`goods_id`) REFERENCES `goods`(`id`)
);
INSERT INTO `history`(`user_id`,`goods_id`,`date`) VALUES
(1,1,'2022/06/10')