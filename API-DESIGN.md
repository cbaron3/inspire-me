# API Design Document

https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design
https://scotch.io/bar-talk/processing-incoming-request-data-in-flask

## Users

-- Get all users    (api/v1/resources/users/all)
-- Get some users   (api/v1/resources/users?filters)
-- Get a user by ID (api/v1/resources/users?<int:id>)
-- Add user         (api/v1/resources/users/allfilters)
-- Put (update) user preferences; confirmed and datetime    (api/v1/resources/users/allfilters)
-- Delete user  (api/v1/resources/users?<int:id>) (api/v1/resources/users/allfilters)

## Quotes

-- Get all quotes   (api/v1/resources/quotes/all)
-- Get some quotes  (api/v1/resources/quotes?filters)
-- Get a quote by ID    (api/v1/resources/quotes?<int:id>)
-- Post (add) quote     (api/v1/resources/quotes/allfilters)
    Check if already exists first. Only post if does not exist
-- Put (update) quote; mainly frequency (api/v1/resources/quotes/allfilters)
    Only update if exists and has valid filters. Only filter is frequency
-- Delete quote (api/v1/resources/quotes?<int:id>)
    Delete by id

## Twilio
-- Send subscribe message to user id    (api/v1/)
-- Receive message for confirming subscription  (api/v1/)

## Misc
-- Get all resources    (api/v1/resources/all)