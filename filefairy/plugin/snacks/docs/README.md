# Snacks

Feeds the masses bread and circuses.

## Getting Started

This feature is accessible from the #snacks channel. There are several
interactions that can be performed.

### Choose

Need some help making a choice?

```
@filefairy choose <foo> or <bar>
```

![Example](images/choose_mets.png?raw=true)

![Example](images/choose_shade.png?raw=true)

### Discuss

Want a nonsensical opinion on a topic?

```
@filefairy discuss <foo>
```

![Example](images/discuss_bunting.png?raw=true)

![Example](images/discuss_loyola.png?raw=true)

### Imitate

Want @user's nonsensical opinion on a topic (or lack thereof)?

```
@filefairy imitate @user
```

![Example](images/imitate_random.png?raw=true)

```
@filefairy imitate @user <topic>
```

![Example](images/imitate_topic.png?raw=true)

### Say

Looking for an echo chamber?

```
@filefairy say <foo>
```

![Example](images/say.png?raw=true)

### Snack Me

Hungry?

```
@filefairy snack me
```

![Example](images/snack_me.png?raw=true)

### Who

Need some help making a choice between users?

```
@filefairy who <foo>
```

![Example](images/who.png?raw=true)

## FAQ

Answers to the questions you didn't know you had.

### I'm trying to spam an interaction. Why am I not getting a response?

Users can only interact with the feature only once every ten seconds. Let it
breathe, okay?

### How does the discuss interaction work?

Public chat history is indexed into a probabilistic n-gram model, which is then 
used to create run-on sentences about whichever topic is supplied.

### ELI5 n-gram models.
You know how your phone's keyboard can write sentences, if you repeatedly tap
the suggested words? It's basically like that.

### Back up, my chat history is being indexed?

Yes, chats in public channels help power the discuss interaction's understanding
of language (for better or worse).

### I'd rather my messages not be used in this way.
Please message brunnerj to opt out.

### I asked for snacks, so why was I served a star?

Stars appear when the two randomly selected snacks are identical. This outcome
occurs roughly ~1.5% of the time.

### What do I win if I have the most stars?

Nothing, because stars aren't saved. Not everything has to be a competition,
alright?
