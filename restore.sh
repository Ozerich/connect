#!/bin/sh
mysqladmin -u root -p drop bsuir
mysqladmin -u root -p create bsuir --default-character-set=utf8
mysql -u root -p bsuir < db
