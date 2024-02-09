DELETE FROM `user`;

ALTER TABLE `user` MODIFY COLUMN `password` VARCHAR(255) NOT NULL;

INSERT INTO `user` (`username`, `email`, `password`) VALUES('水谷有香','youxiangshuigu14.arh2tpvnz@gmail.com','ICjs8G54L9Tu');

