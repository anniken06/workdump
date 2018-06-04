#SingleInstance force

:*:;=::=================================================================================================================
:*:;mci::mvn clean install
:*:;smci::mvn clean install -DskipTests
:*:;gf::git fetch --all
:*:;gs::git stash
:*:;grh::git reset --hard
:*:;gru::git reset --hard @{{}u{}}
:*:;gcb::git checkout 
:*:;gt::git tag ""{Left}
:*:;gpull::git pull
:*:;gpush::git push
:*:;glog::git log --oneline

:*:;sp::
{
	Send, System.out.println();
	Send, {Left}
	Send, {Left}
	Return
}

:*:;cls::
{
	Send, clear
	Send, {Enter}
	Sleep, 1000
	Click, 0, 0, right 
	Send, {DOWN 14}
	Send, {Enter}
	Return
}

^SPACE:: Winset, Alwaysontop, , A
^UP:: WinSet, Style, +0xC00000, A
^DOWN:: WinSet, Style, -0xC00000, A
^RIGHT:: WinHide, A
^LEFT:: WinShow, A
