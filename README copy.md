# Hubuum, a single pane of glass

Hubuum (𒄷𒁍𒌝) in Sumerian translates as “axle” or “wheel assembly”[1]. The goal of Hubuum is to be the main hub for anyone wanting information about ones IT equipment, people, buildings, rooms, or anything else of interest. 

All in one UI, all with one API.

## Concept

There are a million systems out there. They all have their interfaces. They all have their UIs. But we don't want UIs. We want *one* UI that gathers information from all other systems and presents it in ways that are useful.

## Design

Hubuum aims to have a small core of data models that track information gathered from Hubuum modules. Some modules are:

### DNS
  
Gather information from DNS. Are your hosts registered properly in DNS? Do machines and DNS agree on naming setup? 

### [Fleet](https://fleetdm.com) / [osquery](https://osquery.io).

Endpoint visibility. OSquery agents report hardware and software to fleet, which is fetched by Hubuum. How many machines are currently running CPUs with a given heartbleed fix? Is the fix applied? 

### [Zabbix](https://zabbix.com)

Monitoring and status. Has a given machine reported problems in the last month?

### LDAP

User and group data

### Web scrapers

For those moments when you just have to... Maybe your organisation has some data users enter themselves into structured web pages, and that information is only available as html...

### Exchange (+TP)

Calender data for users and rooms.

## The goal

Each system that has data is important, but the goal is to be able to ask about information across these systems...

When first line support gets a call, Hubuum recognizes the number. It's from a meeting room. The room is booked by a person in engineering. Their account shows no flags. They have also booked a video conferencing appointment. Unfortunately, room database shows that there is a problem with the camera in the room and that a replacement is ordered. There are references to tickets from the ticketing system.

Before the conversation even starts, the responder is in a much better place to assist the caller. Right then and there. Without needing to dig for information. 

It is just there. At a glance. From Hubuum.

---


[1] Hubuum in Sumerian is a loanword from Akkadian. Ref: https://sumerianlanguage.tumblr.com/post/681905416832172032/how-do-you-say-wheel-in-sumerian