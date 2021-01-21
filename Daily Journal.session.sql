CREATE TABLE `Mood` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label` TEXT NOT NULL
);

CREATE TABLE `JournalEntries` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept` TEXT NOT NULL,
	`entry` TEXT NOT NULL,
	`date` INTEGER NOT NULL,
	`mood_id` INTEGER NOT NULL,
	FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

INSERT INTO `Mood` VALUES (NULL, "happy");
INSERT INTO `Mood` VALUES (NULL, "sad");
INSERT INTO `JournalEntries` VALUES (NULL, "coding", "it's even harder", 12342343, 2);

SELECT
e.id,
e.concept,
e.entry,
e.date,
e.mood_id,
m.label
FROM journalentries e
JOIN Mood m
ON m.id = e.mood_id
WHERE e.entry LIKE '%';

SELECT * FROM Mood;