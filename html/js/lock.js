var lockTimeout;
var lockTimeoutId;

function lockTimeoutStart() {
	lockTimeout = cfg.lock_timeout_minutes;
	lockTimeoutId = window.setInterval(function() {
		lockTimeout--;

		if (lockTimeout <= 0)
			lock();
	}, 1000 * 60);
}

function lockTimeoutUpdate() {
	lockTimeout = cfg.lock_timeout_minutes;
}

function lockTimeoutStop() {
		clearInterval(lockTimeoutId);
}
