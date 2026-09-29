from random import randint
import reflex as rx

ANECDOTES = [
	"If it hurts, do it more often.",
	"Adding manpower to a late software project makes it later!",
	"The first 90 percent of the code accounts for the first 90 percent of the development time...The remaining 10 percent of the code accounts for the other 90 percent of the development time.",
	"Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
	"Premature optimization is the root of all evil.",
	"Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it.",
	"Programming without an extremely heavy use of print is same as if a doctor would refuse to use x-rays or blood tests when diagnosing patients.",
	"The only way to go fast, is to go well.",
]

class AnecdoteState(rx.State):
	selected: rx.Field[int] = rx.field(0)
	votes: rx.Field[list[int]] = rx.field([0 for _ in range(len(ANECDOTES))])

	@rx.event
	def random_anecdote(self):
		self.selected = randint(0, len(ANECDOTES) - 1)

	@rx.event
	def upvote(self):
		self.votes[self.selected] += 1

	# Getting the most voted for anecdote requires the operations 'index' and 'max'
	# which don't work on Var so it needs to happen as computer var in the class
	@rx.var
	def most_voted_idx(self) -> int:
		return self.votes.index(max(self.votes))

	@rx.var
	def most_voted_anecdote(self) -> str:
		return ANECDOTES[self.votes.index(max(self.votes))]

	@rx.var
	def selected_anecdote(self) -> str:
		return ANECDOTES[self.selected]

def index() -> rx.Component:
	return rx.el.div(
		# ANECDOTES is plain Python and expects an index, where AnecdoteState.selected
		# is a Var, so turn ANECDOTES into a Var
		rx.el.p("Anecdote of the day"),
		rx.el.p(AnecdoteState.selected_anecdote),
		rx.el.p(f"has {AnecdoteState.votes[AnecdoteState.selected]} votes"),
		rx.el.button("upvote", on_click=AnecdoteState.upvote),
		rx.el.button("next anecdote", on_click=AnecdoteState.random_anecdote),
		rx.el.br(),
		rx.el.p("Anecdote with most votes"),
		rx.el.p(f"{AnecdoteState.most_voted_anecdote}"),
		rx.el.p(f"has {AnecdoteState.votes[AnecdoteState.most_voted_idx]} votes"),
	)

app = rx.App()
app.add_page(index)