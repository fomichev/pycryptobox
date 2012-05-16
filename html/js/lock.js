var lockTimeout;
var lockTimeoutId;

function lockTimeoutStart() {
	lockTimeout = _cfg_lockTimeout;
	lockTimeoutId = window.setInterval(function() {
		lockTimeout--;

		if (lockTimeout <= 0)
			lock();
	}, 1000 * 60);
}

function lockTimeoutUpdate() {
	lockTimeout = _cfg_lockTimeout;
}

function lockTimeoutStop() {
		clearInterval(lockTimeoutId);
}
