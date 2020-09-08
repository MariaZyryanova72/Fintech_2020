pragma solidity >=0.5.0 <0.6.0;

contract MyFirstContract {
	uint256 public accumulator;
	uint256 limit = 20;
	address owner = msg.sender;

	event Increased(uint256 newaccumulator);
	event LimitChanged(uint256 newlimit);

	function increase(uint256 _x) public {
		if (((accumulator + _x) > limit) && (msg.sender != owner))
			revert();
		require(accumulator + _x > accumulator);
		accumulator += _x;
		emit Increased(accumulator);
	}

	function changeLimit(uint256 _l) public {
		require (msg.sender == owner);
		limit = _l;
		emit LimitChanged(limit);
	}

	function getState() public view returns (uint256, uint256) {
		return (accumulator, limit);
	}
}