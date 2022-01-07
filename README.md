# SMSpotifY

Just a little tool so that my friends can text a phone number and add to my spotify queue for parties and such:)

## Features

* Roles / Access Control

  * Admin
  
    * Currently the authorization function just returns true for admins, might be subject to change?
    
    * Admins can currently queue tracks as well as whitelist new users

  * End User
  
    * "End User" used to distinguish between the role and the internal mental model (and DB model) I've built up of a User
    
    * End users can currently only queue tracks
    
  * Roles may be subject to change, ideally it'll be as modular and customisable as possible.
  
  * I would also like to implement identity-based access control, or experiment with it
  
    * This will likely end up taking the form of `OperatorService.user_has_perms()` first checking if any permissions are listed in the user object
    
    * If no relevant permissions are found on the user object, the role object would then be checked.
  
* Queueing Tracks
 
  * Required Permission Level: **End User**
  
  * User can text a link to a Spotify album, playlist, or track, and the song(s) will be queued.
  
## Using SMSPotifY

### End Users

* It's as easy as texting a **Spotify** link for any _track_, _playlist_, or _album_ to the appropriate phone number! (Ask your friend who has it setup :) )

### Admins

* Whitelisting new users
  
  * `whitelist name;phonenumber;role`
  
    * Name: Supports full names, will only ever respond with the first name
    
    * Number: +11231231234
    
    * Role: `admin` | `end_user`
    
    * _Currently there's no validation on number or role, so malformed entries will still be submit_
    
## Configuring SMSPotifY

* WIP 🥺🥺
