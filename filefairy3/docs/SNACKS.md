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

![Example](images/snacks_choose_mets.png?raw=true)

![Example](images/snacks_choose_shade.png?raw=true)

### Discuss

Want a nonsensical opinion on a topic?

```
@filefairy discuss <foo>
```

![Example](images/snacks_discuss_bunting.png?raw=true)

![Example](images/snacks_discuss_cardinals.png?raw=true)

### Snack Me

Hungry?

```
@filefairy snack me
```

![Example](images/snacks_snack_me.png?raw=true)

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

Nothing, because stars aren't saved. Not everything has to be a competition...
