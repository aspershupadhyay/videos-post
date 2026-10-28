# Case 023 — post copy (Instagram carousel, 9 slides, 4:5)

Files (VoiceBox, Files → Images): `case-023-moe-slide-01.png` … `case-023-moe-slide-09.png`. Post them in order.

## Caption
> Zuckerberg's newest AI is 400 billion parameters. For each word it writes, it uses 17 billion. That's Mixture of
> Experts, and almost every big model now works this way.
>
> The trick: a tiny "router" scores 128 experts and sends each word to one of them (plus one shared expert). The other
> 127 sit idle. Big model, small bill.
>
> The catch Meta mentions itself: all 400B still have to sit in memory. And the "experts"? When Mistral looked inside
> its own MoE, the router didn't sort by topic at all. It sorted by syntax.
>
> Save this for the next time someone brags about "128 experts."
>
> Sources: Meta, "The Llama 4 herd" (ai.meta.com/blog/llama-4-multimodal-intelligence, Apr 5 2025); Jiang et al.,
> "Mixtral of Experts", §5 Routing analysis (arXiv 2401.04088). Stills: The Social Network (2010, Columbia Pictures),
> used for commentary.
>
> #ai #llm #machinelearning #mixtureofexperts #llama4 #thesocialnetwork

**First comment (pin it):** "Which model should we open up next?" (a question that's easy to answer drives comments).

## Alt text (per slide, for accessibility + search)
1. Jesse Eisenberg as Mark Zuckerberg in a hoodie; headline "Zuckerberg's AI ignores 96% of itself."
2. 64 black squares: a dense model uses every part for every word.
3. One shared expert bar and 128 grey squares, one red: each word visits one shared expert plus one of 128.
4. The ranking formula written on a dorm window in The Social Network; "Every MoE has one too. It's called the router."
5. Four steps: a word comes in, the router scores all 128 experts, the top scorer does the work, the other 127 sleep.
6. Bar: 17B active out of 400B stored, with Meta's sentence underlined.
7. Meta's blog: "all parameters are stored in memory" underlined.
8. Mixtral paper: "we do not observe obvious patterns in the assignment of experts based on the topic" underlined.
9. "Not 128 geniuses. One very fast traffic cop." and the CatchTheError logo.

## X (thread opener)
> Meta's Llama 4 Maverick: 400B parameters, 17B used per token. That's Mixture of Experts.
> The fine print: all 400B still sit in memory (Meta says so), and the "experts" don't split by topic (Mistral's own
> routing analysis). 🧵
