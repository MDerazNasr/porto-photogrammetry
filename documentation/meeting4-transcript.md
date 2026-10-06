# Meeting 4 transcript - 25 September 2026

## Provenance and completeness

This file preserves the Meeting 4 transcript excerpts supplied by Mohamed on 25 September and 2 October 2026. The meeting date is 25 September 2026. The supplied material now covers `0:44-1:19`, `2:01-2:25`, `20:05-23:27`, and `52:05-54:09`. The remaining gaps are explicitly marked. No supplied segment contains a statement by Mohamed, so no personal commitment is attributed to him from missing material.

## Supplied transcript

**0:44 - Anthony Abruzzini:** Hey, good morning.

**0:45 - Ihor Vilkhovyi:** Hi.

**0:46 - Anthony Abruzzini:** Thanks for posting your reports, by the way. It was awesome.

**0:52 - Ihor Vilkhovyi:** Yes. Yeah, I'm in Germany right now.

**0:57 - Anthony Abruzzini:** Oh, cool.

**1:05 - Ihor Vilkhovyi:** You good? How's it going?

**1:08 - Anthony Abruzzini:** Yeah, you're doing great. How about you? How was the travel over there? Are you doing OK?

**1:13 - Ihor Vilkhovyi:** Yes, yes, yeah, all good. Yeah, so just finished with some work now. And yeah, so I'm on vacation next week, so just wrapping up everything now, trying to, yeah.

> **Transcript gap:** `1:19-2:01` was not included in the supplied excerpts.

**2:01 - Syed Rizvi:** Hi, Anthony. How's it going?

**2:05 - Anthony Abruzzini:** Hey, good morning. Doing pretty good. How are you?

**2:08 - Syed Rizvi:** All good, all good.

**2:10 - Anthony Abruzzini:** Yes.

**2:13 - Syed Rizvi:** Where are you based out of?

**2:16 - Anthony Abruzzini:** Seattle, Washington, so...

**2:19-2:23 - Syed Rizvi and Anthony Abruzzini:** Syed reacts to the location; Anthony notes that it is seven in the morning.

**2:25 - Anthony Abruzzini:** Which is better than when I was in Finland; it was three in the morning, so it's a better place to be.

> **Transcript gap:** `2:25-20:05` was not included in the supplied excerpts.

**20:05 - Syed Rizvi:** Florida I have to look at. So that's one concern. Texturing, we've already talked about. And then maybe this is something that all of us should probably look into. I sent a shortlist of papers from various conferences.

**20:25-21:04 - Syed Rizvi:** The deadlines for the shortlisted venues appear achievable. He plans to read the most relevant papers and determine what the project's analysis must include. A table of results alone will not suffice; even dataset papers are framed around evaluations and data, so a significant analysis of where methods fail is likely expected.

**21:25-21:43 - Syed Rizvi:** He recommends that everyone review whichever shortlisted papers are most relevant to their work, or find more relevant papers, to understand what makes a compelling analysis for the publication.

**21:53 - Om Kshatriya:** Asks whether the dataset will be published on MorphoSource or another platform.

**22:08-22:28 - Syed Rizvi:** The dataset must be public for publication. Hugging Face is a viable option; MorphoSource is also possible, although support for all required formats is uncertain.

**22:35 - Om Kshatriya:** Notes that MorphoSource already provides viewers for formats such as PLY, whereas Hugging Face's 3D-viewer support is uncertain.

**22:41-23:02 - Syed Rizvi:** Agrees and closes the question period.

**23:10-23:27 - Group:** Closing remarks. Anthony says the team is on track despite the difficulties and wishes everyone a good weekend.

> **Transcript gap:** `23:27-52:05` was not included in the supplied excerpts.

**52:05 - Syed Rizvi:** Yeah, I mean for the SAM3 jobs, they ran fine. I didn't have to wait at all. So maybe it is being respected.

**52:06 - Ihor Vilkhovyi:** Yeah.

**52:10 - Arthur Porto:** Book. Yeah, yeah, yeah, so if you run into issues, just ping me and then I'll ping them or kill their jobs if it comes to that. Ideally, we would rather talk to them first.

**52:15 - Ihor Vilkhovyi:** Yeah, that's it.

**52:22 - Syed Rizvi:** All right. Sounds good.

**52:27 - Ihor Vilkhovyi:** And so, just so I said that, yes, like to break down this question, I think, like, the main part is availability, right? And yeah, and then the second part that we wanted to have all the specimens and all experiments of the same hardware, so we can compare the whole clock time, right? And also, I think recently we received an e-mail from PACE that they are limiting kind of, you know, the usage, because somebody apparently was running, I don't remember, like 500 jobs.

**52:43-52:53 - Syed Rizvi:** Yes. Mhm. Yeah.

**52:59 - Ihor Vilkhovyi:** Five hundred jobs, yes, so that's like the limit, like from 500 to 50. I hope it was not me or Syed, you know, you guys, yeah. Sounds good.

**53:13-54:09 - Group:** Closing greetings.

**53:22 - Anthony Abruzzini:** I did want to let everybody know, I wrote a Slack bot to grab all your research reports. So if you don't tag me or Riyam, it won't matter. It'll still find them no matter where you post them, how you post them.

**53:36 - Syed Rizvi:** Do we have to use a keyword or anything or will it work?

**53:39 - Anthony Abruzzini:** Nope, it'll find them no matter what you do. So you don't have to do anything other than post it somewhere, somehow.

## Action analysis

- **Mohamed's stated commitments:** none are present in the supplied excerpts. The remaining gaps must be recovered before attributing any personal promise.
- **Publication-analysis review:** Syed asked everyone to read the relevant dataset/benchmark papers and determine what makes an evaluation compelling, especially method-specific failure analysis beyond a score table. The Slack follow-up supplies ECCV 2026, ICML 2026, and NeurIPS 2025 CSV shortlists.
- **Dataset publication:** publication requires a public dataset. Compare MorphoSource and Hugging Face for supported formats, metadata, download/access model, persistent identifiers, licensing, and integrated 3D viewing; MorphoSource's existing 3D viewer is a stated advantage.
- **Compute comparability:** Ihor said availability is the first constraint and that specimens/experiments used for wall-clock comparison should run on the same hardware.
- **Queue etiquette:** Arthur asked researchers to contact him when resource conflicts occur. Communication should precede killing another user's jobs.
- **PACE constraint:** the reported concurrent-job ceiling was reduced from 500 to 50. Confirm the live scheduler policy before launching arrays.
- **Weekly reports:** Anthony's bot finds posted reports without tags or keywords. Posting the attachment is sufficient; the outdated bot description was corrected in Slack after the meeting.
- **Ihor's next technical direction:** his Week 5 report, posted the same day, narrows the coded-marker work to explaining why global static-marker triangulation fails while short windows agree, improving oblique-view decoding, and extending validated scale recovery to the remaining Artec-paired specimens. These are report-derived tasks, not words recovered from the missing transcript segment.
- **Post-meeting direct request from Syed (2 October):** Mohamed and Om should revisit neural implicit surface methods—Neuralangelo, NeuS2, NeuS, and other credible candidates—to broaden the evaluation beyond Meshroom versus 3DGS. Any new trial should use background masking because the older neural-implicit experiments did not, while masking produced the largest gains for 3DGS methods.
