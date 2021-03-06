"""
Functions to deal with partitions
"""

from __future__ import division
from sage.all import RealNumber, RealField, log
import numpy as np
from itertools import chain

__all__ = ["partition_diameter", "equispaced", "step_function", "check_partition", "partition_sizes_log2"]

def is_iterable(x):
	"""
	Check if the given variable is iterable
	"""
	try:
		iterator = iter(x)
	except TypeError:
		return False
	else:
		return True

def partition_diameter(partition):
	"""
	Return `max(partition[i+1]-partition[i])`.
	
	`partition` can also be an integer, in this case returns 1/n (assumes this is a notation for equispaced intervals).

	Returns:
		partition diameter (real, RNDU)

	"""
	if is_iterable(partition):
		m = max(RealNumber(partition[i+1],rnd='RNDU')-RealNumber(partition[i],rnd='RNDU') for i in range(len(partition)-1))
		return RealNumber(m, rnd='RNDU') # Workaround for a Sage bug, the returned parent ring was wrong (http://trac.sagemath.org/ticket/17734)
	else:
		if partition < 1:
			raise ValueError, "Wrong partition dimension. You passed in 1/n instead of n?"
		else:
			return RealNumber(1.0,rnd='RNDU')/partition

def partition_minimum_diameter(partition):
	"""
	Return min(partition[i+1]-partition[i])
	
	Returns:
		minimum diameter (real, RNDD)
	"""
	m = min(RealNumber(partition[i+1],rnd='RNDD')-RealNumber(partition[i],rnd='RNDD') for i in range(len(partition)-1))
	return RealNumber(m, rnd='RNDD')
	
def equispaced(n):
	"""
	Return a partition composed of n equispaced intervals.
	"""
	return np.linspace(0, 1, num=n+1)

def step_function(v, partition):
	"""
	Return a generator for a list of pairs (x,y) that define a step function from an invariant measure v on a partition partition.
	
	The list is in a suitable format to feed to sage.plot_step_function()
	"""
	
	if not is_iterable(partition):
		partition = equispaced(partition)
	
	if len(partition) - len(v) != 1:
		raise ValueError, "v and the partition do not have compatible sizes"
		
	# we chain a last value with 1 at the end so that it looks better when plotted
	last_value = (1,v[-1]/(partition[-1]-partition[-2]))
	return chain(((partition[i], v[i]/(partition[i+1]-partition[i])) for i in range(len(v))), [last_value])

def check_partition(partition):
	"""
	Raise errors unless: the partition is increasing, starts with 0 and ends with 1
	
	`partition` here must contain a real iterable partition, not just a number.
	"""
	
	if partition[0] != 0 or partition[-1] != 1:
		raise ValueError, "The partition does not have endpoints [0,1]"
	
	for i in range(len(partition)-1):
		if not partition[i+1]-partition[i] >= 0:
			raise ValueError, "The partition is not increasing"
	return True

def partition_sizes_log2(partition):
	"""
	return the log-2 of the sizes of each interval in partition
	"""
	return [log(partition[i+1]-partition[i],base=2.0) for i in range(len(partition)-1)]

def hat_control_points(i, partition):
	"""
	control points of the hat function centered in a vertex of the partition.

	Args:
		i (int):
		partition (container):

	Returns:
		(a0, a1, a2): partition[i-1], partition[i], partition[i+1], with suitble wrapping around 0 so that they are sorted
	"""
	if i == 0:
		return (partition[-2]-1, partition[0], partition[1])
	else:
		if i==len(partition)-1:
			return (partition[-2], partition[-1], partition[1]+1)
		else:
			return (partition[i-1], partition[i], partition[i+1])

def is_refinement(fine_p, coarse_p):
	"""
	Check if a partition is a refinement of a previous one

	Args:
		fine_p:
		coarse_p:
	"""

	# not so important to have it rigorous
	return set(coarse_p).issubset(set(fine_p))