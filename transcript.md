Chapitre 1 : Le wiki LLM (idée de Karpathy)
0:00A couple months ago, Andre Karpathy released the idea of the LLM wiki. It's a pattern for building personal knowledge bases using LLMs and it totally took off and for good reason.
0:1111 secondesThere's a lot of power in the simplicity here. So, this single markdown document in GitHub called it gist got to 40,000
0:1818 secondesstars. And seriously, you can take this file, copy it, paste it into your coding agent, and ask it to build you an LLM wiki and it's going to be able to just
0:2626 secondesbasically oneshot it. So, it's really easy to get started. And the idea here is when we're building a personal knowledge base for our second brain,
0:3535 secondesinstead of just dumping in a bunch of documents or indexing things for rag, we can have the LLM help us build something smarter, incrementally building and
0:4343 secondesmaintaining a persistent wiki with structured interlink collections of markdown files. And so the idea here is as we're adding in more sources over
0:5252 secondestime like meeting transcripts, plan documents, articles from online, it's going to not just index it, but it's going to read each file, extract key
1:011 minute et 1 secondeinformation, and integrate it into the existing wiki. So updating things like the entity pages that it creates over time, so we have that knowledge graph
1:091 minute et 9 secondesfor agent to traverse through and remember all the important information that we're bringing in. So, at this point, pretty much everybody is building
1:161 minute et 16 secondestheir own LLM wiki in their second brain. But this isn't enough. And the main problem that we have here is when you take this gist and you build your
1:251 minute et 25 secondesown version of an LLM wiki, it's going to be structured differently than the next person doing the same thing.
1:311 minute et 31 secondesThere's no standard. And so, there's really not a way to share your LLM wiki with someone else. And that's a bummer.
1:371 minute et 37 secondesYou can think of a lot of different use cases where you'd want to curate a knowledge base over time and then share it with other people like other people on your team. Maybe you want one wiki
1:451 minute et 45 secondesfor the team that everyone's second brains are accessing independently.
1:491 minute et 49 secondesMaybe I want to create a wiki for my YouTube content and then share that with you. There are a million reasons. But if your agent doesn't know exactly how I've
1:581 minute et 58 secondesstructured my wiki with the different metadata and my entity files, it's not going to be able to search through it optimally. We need a standard so that
Chapitre 2 : Pourquoi avons-nous besoin d'une norme ? OKF de Google
2:052 minutes et 5 secondeseveryone's building wikis in the same way so that we can share them freely.
2:102 minutes et 10 secondesAnd so that is what Google has released here with their open knowledge format.
2:142 minutes et 14 secondesIt is a beautifully simple thing just like Harpathy's LLM wiki idea where it's just a simple standard built on top so
2:222 minutes et 22 secondesthat you can guarantee you're building your wiki in a way where other people's second brains can understand it and vice versa. And so in this video I want to
2:312 minutes et 31 secondescover why OKF is so powerful. It really is the future of personal agents. And I want to show you how easy it is to get started with this standard, both for new
2:402 minutes et 40 secondesLM wikis and even transferring existing ones into this format. Very easy to do that. And no matter the wiki, no matter how much you're going to share it or
2:482 minutes et 48 secondesnot, this is important even as an optimization on top of Karpathy's LM wiki idea. And I know that Google is
2:562 minutes et 56 secondeslagging in the AI race right now. Gemini is not as good as GPT and Claude, but they have been releasing some really good stuff on how to leverage LLMs
3:043 minutes et 4 secondeseffectively. And I think that's a totally different lane than building LLMs. Well, so I think this is something really worth leaning into even if OKF
3:133 minutes et 13 secondesdoesn't end up becoming the standard down the line for personal agents. There's going to be something like this. And so it's good to understand this now.
Chapitre 3 : Ce qu'OKF normalise
3:203 minutes et 20 secondesOkay. Now, let's really get into OKF. So there are two things that they're standardizing here. The first is how we are organizing information like our
3:283 minutes et 28 secondesentity documents and our concepts. And then the second standardization is the exact fields that we're going to have in
3:353 minutes et 35 secondesour metadata. So this is the information that we tag at the top of every single document to give the agent a richer set
3:433 minutes et 43 secondesof information. So we can even like query based on the title or the tags. So we have categorization. This is one of the most important things to let the
3:503 minutes et 50 secondesagent traverse through our wiki like a knowledge graph. And really the best way to make this concrete for you is to show
3:573 minutes et 57 secondesyou what a traditional Karpathy wiki looks like. So we'll take a look at this. This is one of the first wiks that I built when Karpathy released this
4:054 minutes et 5 secondesidea. And then we'll get into some of the problems that we have here. So at the top of every single wiki is your index file. You have the agent maintain
4:144 minutes et 14 secondesthis every single time it's bringing new information in. And the index file, it reads this when it's first searching through your knowledge base, pretty much
4:214 minutes et 21 secondesevery single time. And so this just gives you a high-level overview of all the documents that you have access to in the wiki. So the article and then a
4:304 minutes et 30 secondesquick summary so it knows if this is something that it should look into based on the user's request. And so every single time we add in new documents,
4:374 minutes et 37 secondesthis is evolving. And so the agent will read this and then based on what we asked it to do or the question, if it figures like I should look at superbase
4:454 minutes et 45 secondeso this concept right here, this entity document, then it'll drill into this. We also have the metadata like I talked about earlier like the title and the
4:534 minutes et 53 secondestags so that it can also search based on this like if it wants to look at the category of security then it can filter
5:005 minutesout just those documents and so then we have the full sort of like skill.md here this is like progressive disclosure like
5:075 minutes et 7 secondesskills where the index tells it the knowledge it has and then it can read the full document if it's appropriate and then we also link to related
5:155 minutes et 15 secondesconcepts down here and that link is what really gives us this graph view where You can see how all of our entities and other documents are connected together.
5:245 minutes et 24 secondesSo, the agent can sift through this to really get a comprehensive set of information if the question really calls for it. And so, looking at one of these
5:325 minutes et 32 secondesdocuments here, it might feel like it's overwhelming to build up all this knowledge over time, but seriously, with an LLM wiki, you are just giving the
5:405 minutes et 40 secondesreins completely over to an LLM. So, you don't have to be technical. You don't have to spend a lot of time maintaining this. Literally the whole benefit of the
5:485 minutes et 48 secondeswiki is that up until we've had LLMs for this, it was way too tedious to create this sort of knowledge base where we're
5:565 minutes et 56 secondesresponsible for understanding related concepts and building that over time as we're adding in new information. Like there's so much tedious work here that LLM are really, really good at. But as
6:056 minutes et 5 secondesmuch as they're good at this, they aren't going to create this system in the same way that someone else will with with their LLM, right? like the way that
6:146 minutes et 14 secondeswe link related concepts might be different. The way we structure information, even the metadata, like what if we don't have tags, but we have
6:226 minutes et 22 secondesa field called categories. I mean, even something as simple as that, that that little change might make it so that if I gave the knowledge base to another
6:296 minutes et 29 secondesperson's agent, it wouldn't know how to search through things categorically. It would have to dive into the metadata
6:366 minutes et 36 secondesfirst to understand that, and it might not decide to do so. I mean, all these little problems will start to compound when you don't have the same metadata, you don't have the same folders. That's what we're looking to do here with OKF.
Chapitre 4 : Créer avec la spécification OKF
6:476 minutes et 47 secondesAll right. So now, if you want to build with OKF, create a new knowledge base with this format or even refactor one to use the open knowledge format, look no
6:566 minutes et 56 secondesfurther than their spec.md file. So, this is in their repo. I'll link to it in the description. This is just like Karpathy's gist where you copy this
7:057 minutes et 5 secondesdocument. Like you literally just click this one button right here, put it into your coding agent, and tell it to either build you a wiki following the open
7:127 minutes et 12 secondesknowledge format or even refactor an existing one. Like I said, it's going to knock either of those out of the park because this is kind of like a skill. It
7:207 minutes et 20 secondesteaches the coding agent everything it needs to know about the standard. Like here is the terminology. Here's how we structure the bundles. I'll show you
7:277 minutes et 27 secondesmore on this in a little bit. Here is how we build the YAML front matter.
7:317 minutes et 31 secondesdifferent attributes that we have for each one of our documents like the tags for categorization, right? Like this single source of truth is all that it
7:407 minutes et 40 secondesneeds. And because it's such a simple format, a simple standard overall, it's not really going to get confused going through this. I mean, it's a pretty long
7:487 minutes et 48 secondesfile, but in terms of what large language models can handle these days, especially with, you know, GPT 5.5 or Opus 4.8, this is not much instruction.
7:567 minutes et 56 secondesAnd it it also doesn't really matter the scale of your current knowledge base if you are refactoring because you can
8:038 minutes et 3 secondesspecifically ask it to use sub agents to work through the different sections of your knowledge base to refactor it to this format. So really easy to scale,
8:128 minutes et 12 secondesreally easy to just have the agent rip through this spec. The sponsor of today's video is Post Hog, a single place for you to understand how users
Chapitre 5 : Sponsor : PostHog
8:208 minutes et 20 secondesare actually using your application to debug and fix issues and test and roll out all of your changes. And I'm excited for this because I am using Post Hog
8:298 minutes et 29 secondesmyself in Archon, my open-source AI coding harness builder. I'm legitimately leaning on the data insights that I get
8:368 minutes et 36 secondesfrom Post Hog every single day so that I know exactly how to improve Archon in the way that users actually need. And installing Posthog is incredibly easy.
8:458 minutes et 45 secondesYou just click on the install with AI button on their homepage that I'll have linked to in the description and boom, it's a single command you can run a
8:528 minutes et 52 secondeswizard that will essentially be a senior engineer helping you set up analytics for your entire application in just minutes. And you can also create custom
9:019 minutes et 1 secondedata views like this is the dashboard that I'm looking at every single day to see how people are actually using Archon. And then we can also drill down
9:089 minutes et 8 secondesto get very granular as well. So the individual runs of Archon, I can click into this here to see all the details.
9:159 minutes et 15 secondesAnd so we can go very high level all the way to individual parameters as we need. It's got the analytics for everything.
9:229 minutes et 22 secondesAnd so production is the time where you can't be flying blind. When you have something deployed out to the world, you need observability. And Post Hog is the
9:319 minutes et 31 secondesbest for that. So I'll have a link in the description. I would highly recommend checking them out. And I talked about this a little bit at the start of the video, but this really is
Chapitre 6 : Pourquoi OKF ? Points importants (même si vous ne les partagez jamais)
9:399 minutes et 39 secondesthe future of personal agents. It's like what MCP did for agentto tool communication, this OKF is doing for agent to knowledgebased communication.
9:509 minutes et 50 secondesAnd one of the most important things in the spec here is that they talk about it being a standard both for consuming knowledge bases like searching through
9:579 minutes et 57 secondesthem, but also producing knowledge bases. How do we evolve the wiki over time? build up the entity pages like Karpathy talked about in the initial
10:0610 minutes et 6 secondesgist. We really are building on top of it. And one of the really interesting things to think about here is yes, this
10:1310 minutes et 13 secondesis fantastic for sharing knowledge bases or having a teamwide knowledge base.
10:1810 minutes et 18 secondesThis is also really good though even if you're never going to share a knowledge base. Think about this. If everybody has the same standard for how they are
10:2510 minutes et 25 secondesbuilding up their own personal knowledge base, everyone can share ideas more like, oh, here are the entity pages that
10:3310 minutes et 33 secondesare working really well for me and this is how I want to organize things under the standard. And then because you have the standard as the foundation, it's easier for other people to take those
10:4110 minutes et 41 secondesideas. And so what we're also I think what we're going to see is like yes, I don't think OKF is going to in the end be the standard, but we're going to see
10:4810 minutes et 48 secondessomething like that and we're going to see the standard evolve over time so that it's easier and easier for people to create these really rich knowledge
10:5610 minutes et 56 secondesbases without having to spend a lot of time upfront designing it with the LLM.
Chapitre 7 : Le cadeau : Mon pack de programmation IA
11:0111 minutes et 1 secondeNow, of course, sharing wikis with other people is the biggest benefit of OKF.
11:0511 minutes et 5 secondesAnd that leads me into the example that I have for you that's also a gift I'm very excited to share. I have built a
11:1311 minutes et 13 secondesbundle, that's what you call an OKF Wiki, that packages up all of my favorite AI coding YouTube videos on my
11:2011 minutes et 20 secondeschannel. And so, here's the thing. I'm excited for this. I know that a lot of you, you don't watch my entire video every single time. You're going to sift
11:2911 minutes et 29 secondesthrough things. You're going to just take the transcript and feed it into your second brain and ask questions. You guys are already doing something like this, but now making it easier for you
11:3711 minutes et 37 secondesbecause I'm prepackaging up sets of videos. I actually want to start doing this so that you can very easily bring it into your second brain and ask
11:4511 minutes et 45 secondesquestions as it relates to what you actually care about or what you are working on specifically. And so take a look at this. All you have to do is
11:5311 minutes et 53 secondesfirst of all take this spec and give it to your coding agent. You have it teach itself OKF. And then you go to this repo
12:0012 minuteswith my AI coding knowledge bundle. I'll have this linked in the description as well. And you just paste this prompt into your coding agent. That's it. You
12:0812 minutes et 8 secondesgive it the link to this repo. You tell it to read the readme and set up everything and it already understands OKF. So, it links those two things
12:1512 minutes et 15 secondestogether. Brings the bundle into your local Obsidian or Notion or whatever you're managing your knowledge. And then boom, you can instantly start asking
12:2312 minutes et 23 secondesquestions. You don't have to bring in the transcripts yourself. This is the easiest way for just content creators in general to share their knowledge with
12:3112 minutes et 31 secondesthe world. They can create bundles. I'm creating bundles for all my videos now.
12:3512 minutes et 35 secondesAnd so this is just one example of what OKF unlocks for us. And so I'll also show you what this bundle looks like because it's a really good example of
12:4312 minutes et 43 secondeswhat OKF is really doing for us. All right, let's get into the belly of the beast. Now I'll show you how I've been setting up OKF and we'll get into the
12:5012 minutes et 50 secondesexample bundle as well. And so something that I do for my second brain, every single system that I build in, I always have a tople document that talks about
12:5912 minutes et 59 secondeshow it works. Like this is how I'm working with OKF bundles. And then here are the different bundles that I have.
13:0513 minutes et 5 secondesSo I basically have an index so it knows the different bundles that it can go into and search and read the index that we have in there. So we kind of have
13:1213 minutes et 12 secondeslike two layers of indexing. And then I also built a simple CLI script. This is actually there in the example bundle
13:2013 minutes et 20 secondesthat you can clone that makes it easy for it to in the command line list out my bundles to view a specific index and then you know once it finds one of those
13:2813 minutes et 28 secondesfiles it wants to read then we have the command line tool to read by a specific bundle and concept ID. So I've added
13:3613 minutes et 36 secondeslike a little bit of organization on top of OKF with just how I manage many different bundles but otherwise I'm
13:4313 minutes et 43 secondesfollowing the format exactly. And so let's actually look at one of these.
13:4613 minutes et 46 secondesI'll click into bundles here and we'll go into the one that I just shared the GitHub for. So, if we look at the index here, we can see that I have two
13:5513 minutes et 55 secondesdifferent sections and this is actually a smaller bundle. So, I didn't want to do something super complicated. So, there really are just two sections. I have the videos that I've put in this bundle, which it's it's rather small.
14:0614 minutes et 6 secondesThere's only four videos, but these are like the best and most up-to-date ones on my channel for AI coding. And then I have the concepts as well. So different
14:1414 minutes et 14 secondesthings that I talk about throughout multiple of the videos that I want to extract into its own entity page. And so
14:2214 minutes et 22 secondesthe index here says here are the sections. And then I don't actually have a list of each one of the individual files because I'm just going to have the
14:2914 minutes et 29 secondesagent read the files that we have in concepts or videos, right? Like it can list out here are all the files or it can read the index within concepts
14:3814 minutes et 38 secondesitself, right? So, however you want it to navigate, it's going to be able to go through these different layers of documents or just do a keyword search.
14:4514 minutes et 45 secondesAnd so, clicking into any one of these, like the PIV loop, for example, this is the primary mental model that I always teach for AI coding. Very important to
14:5314 minutes et 53 secondeshave a process for yourself to plan, implement, and validate whatever you're creating with a coding agent. And so, we have the YAML front matter at the top.
15:0215 minutes et 2 secondesAnd the type, this is what is required by OKF. It is the single required field in the metadata because this is what gives categorization to your documents.
15:1215 minutes et 12 secondesSo like this is the type of concept. If I go to a video here, the type is video.
15:1715 minutes et 17 secondesSo we can search over just the videos over just the concepts which is especially powerful once you get bundles that are a lot bigger than this. Again,
15:2415 minutes et 24 secondesthis is just an example here. But then we also have all of the optional titles in OKF. So title, tags, related videos.
15:3115 minutes et 31 secondesThis is how we link things together, right? Like you saw with that other wiki I showed earlier, it was just things were linked at the bottom. However, this
15:3915 minutes et 39 secondesnow makes it so it's easier to navigate, creating a standard for how we are linking our entities together. And so each one of these are optional. Only
15:4815 minutes et 48 secondestype is required in OKF. But just because you don't always have these doesn't mean that your agent won't understand it, right? Like if your agent
15:5615 minutes et 56 secondesis a consumer of OKF, if you gave it the spec and taught it to be a consumer, it's going to know how to leverage these fields for better searching and
16:0416 minutes et 4 secondestraversing through the knowledge graph that we have here. And so then this is just all of our information on the piv loop. I kept it nice and simple. And
16:1116 minutes et 11 secondesthen also linking to videos as well, which maybe is like a little bit redundant with related videos. So I could probably make this bundle a bit better, but I just wanted to have this
16:2016 minutes et 20 secondesas an initial example. And it is something that you can immediately bring into your second brain. Just start asking questions. Like I'll show you an
Chapitre 8 : Observer mon deuxième cerveau l'interroger
16:2616 minutes et 26 secondesexample here in my terminal. So first of all, at the top level of my second brain, I just asked what bundles do I have? It ran a command here. So it used
16:3516 minutes et 35 secondesthat little CLI tool to list out all the bundles that I have. And then it told me that and then I just asked it a question. So not even telling it what
16:4216 minutes et 42 secondesbundle specifically to look through. I said, "What's Cole's single biggest idea for getting reliable code out of an AI coding assistant?" and it ran four
16:5016 minutes et 50 secondescommands in total. So first of all it decided to read the coal AI coding index that's the GitHub that I have for you
16:5716 minutes et 57 secondesand then based on the index it knew like okay let's take a look at the concepts here and then from the concepts it's like okay the single most important
17:0417 minutes et 4 secondesthing I don't know what in the index told it that but it's like context engineering let's read the concept of context engineering so we can see the
17:1217 minutes et 12 secondesprogressive disclosure as the agent is figuring out where it needs to look down to find the answer for me and then we
17:1917 minutes et 19 secondesget the final answer here So just beautiful to watch it work. When we have something structured like this, it's so easy for it to start with really not
17:2717 minutes et 27 secondesmuch context at all and then drill down into exactly what we need. That's what OKF gives us as a standard. All right.
Chapitre 9 : OKF est-il trop simple ?
17:3417 minutes et 34 secondesSo if you're not sold on the idea of having a standard for the LM wiki at this point, I don't know what to tell you. The one critique that I think is
17:4317 minutes et 43 secondesactually pretty valid with OKF is a lot of people are saying that it's too simple, right? like there's not a lot of value or substance that's actually added
17:5117 minutes et 51 secondeson top of the Karpathy wiki. So, I've I've seen that a few times just as I've been doing a lot of research. I mean, I put a lot of time into prepping for
17:5917 minutes et 59 secondesthese videos. I think it's kind of valid because if we look at like what it's really doing on top of the Carpathy wiki, it's it's speaking to like exactly how you organize your different files.
18:0918 minutes et 9 secondesLike they they specifically have like indexes within the folders and a top level index like you saw in my bundle. I mean, that's something I didn't really
18:1618 minutes et 16 secondeshave in wikis before. And then we have the specific fields in our metadata like the type is required. The other ones are optional but these are the ones that
18:2418 minutes et 24 secondesthey recommend. Like that's pretty much it. It's how we organize and what is the metadata. That's pretty much all that we
18:3018 minutes et 30 secondesactually have in the standard. And so like the argument is kind of valid where it's like what is it really giving? Like there's there's not much there. But I
18:3918 minutes et 39 secondesthink that's also the point, right? Like minimally opinionated. It's the bare minimum layer that we need on top so
18:4718 minutes et 47 secondesthat we can produce and consume these wiks in exactly the same way across everyone's agents that lean into OKF.
18:5518 minutes et 55 secondesLike I think that's actually a good thing. I think that's a benefit, not a downside. The fact that there's not much substance here might seem counterintuitive, but I think that is
19:0319 minutes et 3 secondesactually a good thing. And I encourage you just try out the bundle that I have for you here. give it the spec and then give it this prompt and then just start
Chapitre 10 : À vous de jouer + Conclusion
19:1119 minutes et 11 secondesasking questions about AI coding like how I use sub aents uh what is the piv loop like just start asking and and seeing how easy it is for your agent to
19:2019 minutes et 20 secondesgrab those things for you and so that's everything that I got for you today on OKF really is the future of personal agents if you appreciated this video
19:2919 minutes et 29 secondesyou're looking forward to more things on AI coding and second brains I'd really appreciate a like and a subscribe and with that I will see you in the next video.

