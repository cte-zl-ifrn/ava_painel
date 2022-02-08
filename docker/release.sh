#!/usr/bin/env bash
FULL_IMAGE_NAME="ifrn/avaportal"
PROJECT_NAME=avaportal
if [ $# -eq 0 ]; then
  echo ''
  echo 'NAME '
  echo '       release'
  echo 'SYNOPSIS'
  echo '       ./release.sh [-l|-g|-p|-a] <version>'
  echo 'DESCRIPTION'
  echo '       Create a new release $PROJECT_NAME image.'
  echo 'OPTIONS'
  echo '       -l         Build only locally'
  echo '       -g         Push to Github'
  echo '       -d         Registry on Docker Hub'
  echo '       -a         Push and registry on Github'
  echo '       <version>  Release version number'
  echo 'EXAMPLES'
  echo '       o   Build a image to local usage only:'
  echo '                  ./release.sh -l 1.0'
  echo '       o   Build and push to GitHub:'
  echo '                  ./release.sh -g 1.0'
  echo '       o   Build and registry on Docker Hub:'
  echo '                  ./release.sh -d 1.0'
  echo '       o   Build, push to Guthub and registry on PyPi:'
  echo '                  ./release.sh -a 1.0'
  echo "LAST TAG: $(git tag | tail -1 )"
  exit
fi

OPTION=$1
VERSION=$2

build_image() {
  printf "\n\nBUILD local version $FULL_IMAGE_NAME:latest\n"
  docker build --progress=plain -t $FULL_IMAGE_NAME:$VERSION --force-rm .
}

push_to_docker_hub() {
  if [[ "$OPTION" == "-d" || "$OPTION" == "-a" ]]
  then
    printf "\n\nDOCKER HUB project $PROJECT_NAME v$VERSION\n"
    docker login \
    && docker push $FULL_IMAGE_NAME:$VERSION
  fi
}

push_to_github() {
  if [[ "$OPTION" == "-g" || "$OPTION" == "-a" ]]
  then
    printf "\n\nGITHUB: Pushing\n"
    git tag $VERSION \
    && git push --tags origin master
  fi
}

build_image \
&& push_to_docker_hub \
&& push_to_github \

echo $?
echo ""
echo "Done."
