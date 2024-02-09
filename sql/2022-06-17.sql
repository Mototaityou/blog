CREATE TABLE `posts`(
  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `title` VARCHAR(50) NOT NULL COMMENT 'タイトル',
  `content` JSON NOT NULL COMMENT 'ブログ内容',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE `user`(
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `username` VARCHAR(50) NOT NULL UNIQUE COMMENT 'ユーザー名',
  `password` VARCHAR(255) NOT NULL UNIQUE COMMENT 'パスワード',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO `posts` (`title`,`content`)
VALUES('タイトル','{"html":"<p>試し</p>"}');

INSERT INTO `posts` (`title`,`content`)
VALUES('タイトル','{"html":"<p>試しtitle2</p>"}');

ALTER TABLE `posts` ADD COLUMN `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE `posts` DROP COLUMN ``;

ALTER TABLE `posts` DROP COLUMN `updated_at`;
ALtER TABLE `posts` ADD COLUMN `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE `posts` ADD COLUMN `blog_image` BLOB;

ALTER TABLE `posts` DROP COLUMN `blog_image`;

ALTER TABLE `posts` ADD COLUMN `blog_image` LONGBLOB;

ALTER TABLE `posts` ADD COLUMN `image_path` VARCHAR(225) NOT NULL;
ALTER TABLE `posts` DROP COLUMN `image_path`;

UPDATE `posts` SET `image_path` = 'images/Pythonを選んだ理由.001.png' WHERE id = 1;

UPDATE `post`
SET `content`= '{"html":"<p>私の営業事務スキルでは老後2000万円問題を到底解決出来そうもないので、<br>稼げそうなプログラマーに転職しようと思ったため。<br><br>随分前から家計簿をデジタルで入力していたので、自分の稼ぎで老後2000万円問題を<br>解決できるかどうか分からず、ファイナンシャルプランナーに相談しました。<br>結果は「今の資産、給料では到底無理。少なくとも今の年収プラス200万円必要です」<br>と助言をいただきました。<br><br>アラフィフ女性で事務職として今すぐ年収プラス200万円の職に転職する、<br>と言うのは私のスキルではあまりにも無理筋ということが転職サイトに登録して<br>思い知らされました。<br>どうしたら良いか分からなかったので、キャリアカウンセラーに相談しました。<br>結論として「そもそも事務職に向いていないのではないか、長く働ける<br>職種を探すことを検討した方が良い」とアドバイスをもらいました。<br><br>ネットでアラフィフの転職を検索していたら「LIFE SHIFT」という本を読め！という<br>熱いブログを複数見つけたので読んでみました。感想は「私にはやっぱり転職が必要！」と<br>決意を新たにしました。<br><br>さまざまな助言から私が転職先に望むことは<br><br><ol><li>重いものを持つ必要がない事（緑内障のため、重い物を持つと失明の可能性が高いから）</li><br><li>リモートワークができること（将来、両親の介護を見据えて）</li><br><li>今の年収プラス200万円の給与</li><br><li>アラフィフ、未経験でも雇ってもらえる可能性がある職種</li></ol><br>上記に当てはまる職をネットで検索していたらプログラマーという職を見つけました。<br>勉強すれば雇ってもらえそう、という事が分かったのでプログラミングの勉強をしようと<br>決意しました。<p>"}'
WHERE id=2;

